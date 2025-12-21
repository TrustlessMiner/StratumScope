from datetime import datetime

def normalize(source_type, data):
    try:
        if source_type == "stratum_work":
            ntime = data.get("ntime")
            prev_hash = data.get("prev_hash")
            
            # Convert stratum.work hash to standard byte order (reverse it)
            if prev_hash:
                prev_hash = reverse_hash_bytes(prev_hash)
            
            return {
                "source": "stratum_work",
                "job_id": data.get("job_id"),
                "prevhash": prev_hash,
                "timestamp": _safe_ts(ntime or data.get("timestamp"))
            }

        elif source_type == "observer":
            # Observer hash is already in the correct byte order
            return {
                "source": "observer",
                "job_id": None, # Observer doesn't provide actual job IDs. Maybe do away with job_id entirely?
                "prevhash": data.get("prev_hash"),
                "timestamp": _safe_ts(data.get("job_timestamp") or data.get("header_time"))
            }

    except Exception as e:
        print(f"[normalize:{source_type}] ERROR: {e}")

    return None


def reverse_hash_bytes(hash_string):
    """
    Reverse the byte order of a hex hash string using 32-bit word reversal.
    
    Bitcoin hashes in stratum.work are reversed in 32-bit (4-byte) chunks.
    This converts from stratum.work format to standard block explorer format.
    
    Example:
    Input:  "e81c2ee88c4e6e2f2273a86de13e0e926911f9a100001f4b0000000000000000"
    Output: "000000000000000000001f4b6911f9a1e13e0e922273a86d8c4e6e2fe81c2ee8"
    """
    try:
        if not hash_string or len(hash_string) != 64:
            return hash_string
        
        # convert to lowercase
        clean_hash = hash_string.strip().lower()
        
        # Split into 32-bit words (8 hex chars each) and reverse the order
        words = []
        for i in range(0, len(clean_hash), 8):
            words.append(clean_hash[i:i+8])
        
        # Reverse the order of the 32-bit words and join
        reversed_hash = ''.join(reversed(words))
        
        return reversed_hash
        
    except Exception as e:
        print(f"[reverse_hash_bytes] ERROR: {e}")
        return hash_string


def _safe_ts(raw_ts):
    try:
        if not raw_ts:
            return 0.0
        if isinstance(raw_ts, (int, float)):
            return float(raw_ts)
        if isinstance(raw_ts, str):
            if raw_ts.isdigit():
                return float(raw_ts)
            # Handle hex-formatted timestamp (which is common in stratum_work)
            return float(int(raw_ts, 16))
    except:
        return 0.0


def test_hash_reversal():
    """Test function to verify the hash reversal works correctly"""
    
    print("🧪 TESTING HASH REVERSAL")
    print("=" * 50)
    
    # actual data from the websocket test
    observer_hash = "000000000000000000001f4b6911f9a1e13e0e922273a86d8c4e6e2fe81c2ee8"
    stratum_hash = "e81c2ee88c4e6e2f2273a86de13e0e926911f9a100001f4b0000000000000000"
    
    print(f"Observer hash:    {observer_hash}")
    print(f"Stratum hash:     {stratum_hash}")
    
    # Reverse the stratum hash
    reversed_stratum = reverse_hash_bytes(stratum_hash)
    print(f"Reversed stratum: {reversed_stratum}")
    
    # Check if they match
    if observer_hash == reversed_stratum:
        print("✅ SUCCESS! Hashes match after reversal")
    else:
        print("❌ FAILED! Hashes don't match even after reversal")
        print(f"Expected: {observer_hash}")
        print(f"Got:      {reversed_stratum}")
    
    # Test with problematic data
    print("\n🔍 Testing with your latest data:")
    new_observer = "00000000000000000000af03030b362b4cfbe8d5c398e4004851e6c74cdde589"
    new_stratum = "000000000000000003af00002b360b03d5e8fb4c00e498c3c7e6514889e5dd4c"
    
    print(f"New observer:     {new_observer}")
    print(f"New stratum:      {new_stratum}")
    
    reversed_new = reverse_hash_bytes(new_stratum)
    print(f"Reversed new:     {reversed_new}")
    
    if new_observer == reversed_new:
        print("✅ SUCCESS! New hashes match after reversal")
    else:
        print("❌ FAILED! New hashes don't match - may not be byte order issue")
        
        # Check if they're actually different blockchain states
        print("\n🔍 Detailed analysis:")
        print("This might indicate:")
        print("1. Sources are actually on different blockchain forks")
        print("2. Different timestamp windows (one source has newer data)")
        print("3. Another data format issue beyond simple byte reversal")
        
        # Show the differences
        print(f"\nFirst 20 chars comparison:")
        print(f"Observer: {new_observer[:20]}")
        print(f"Reversed: {reversed_new[:20]}")
        print(f"Original: {new_stratum[:20]}")


def test_normalizer_with_real_data():
    """Test the normalizer with your real websocket data"""
    
    print("\n🧪 TESTING NORMALIZER WITH REAL DATA")
    print("=" * 50)
    
    # Real observer data from test
    observer_data = {
        "pool_name": "0xB10C Pool",
        "prev_hash": "000000000000000000001f4b6911f9a1e13e0e922273a86d8c4e6e2fe81c2ee8",
        "coinbase_tag": "ckpool",
        "height": 902003,
        "job_timestamp": 1750399830,
        "header_time": 1750399829
    }
    
    # Real stratum.work data from test
    stratum_data = {
        "_id": "cb9da859-226d-4e83-8bf4-3525e39c14a3",
        "timestamp": "184aab66a74948e7",
        "pool_name": "MARA Pool",
        "height": 902003,
        "job_id": "qLx8QM9SCdDevdRpxBuPSpUneg9DD1qdbVCfx8kzKcjyERsgLErfo3vxAatk",
        "prev_hash": "e81c2ee88c4e6e2f2273a86de13e0e926911f9a100001f4b0000000000000000",
        "ntime": "6854fb76"
    }
    
    print("📊 Testing Observer normalization:")
    observer_result = normalize("observer", observer_data)
    print(f"Result: {observer_result}")
    
    print("\n📊 Testing Stratum.work normalization:")
    stratum_result = normalize("stratum_work", stratum_data)
    print(f"Result: {stratum_result}")
    
    print("\n🔍 Hash comparison:")
    if observer_result and stratum_result:
        obs_hash = observer_result.get("prevhash", "").lower().strip()
        str_hash = stratum_result.get("prevhash", "").lower().strip()
        
        print(f"Observer prevhash:     {obs_hash}")
        print(f"Stratum_work prevhash: {str_hash}")
        print(f"Hashes match: {'✅ YES' if obs_hash == str_hash else '❌ NO'}")
        
        if obs_hash == str_hash:
            print("\n🎉 SUCCESS! The normalizer now produces matching hashes!")
        else:
            print("\n❌ Still not matching - need further investigation")
    else:
        print("❌ Normalization failed")


if __name__ == "__main__":
    test_hash_reversal()
    test_normalizer_with_real_data()