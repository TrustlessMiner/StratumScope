## StratumScope

This is a monitoring and comparison tool for Stratum job broadcasts from multiple Bitcoin mining pools. From this miners can detect job inconsistencies in real-time.

## Purpose

Mining pools should relay accurate and timely block templates to miners. Discrepancies in job announcements could signal non-transparent behavior. The discrepancies could theoritically be due to latency, censorship, or manipulation.

**Key Insight**: Comparing `prevhash` values across the indepedent monitors can allow instant detection of wrong chains.

## Why This Matters

Miners make huge investments into hardware and energy but barely have sufficient `real-time visibility` into whether the work they are receiving is consistent or valid. They rely on pool-provided block templates, but have little insight into their accuracy across the network. This tool is an effort to assist:

- **Solo miners and farms** to see if they are not receiving stale data and that they are at par with consensus chain.
- **Developers and researchers** to identify systemic issues in job distribution.
- **General mining enthusiasts and advocates** to gain a tool to audit pool behavior transparently.

---

## Quick Setup (Run Locally)

Follow these simple steps to run locally:

### 1. Clone the repository

```bash
git clone https://github.com/TrustlessMiner/blockstream-analyzer.git
cd blockstream-analyzer
```
### 2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
pip install -r requirements.txt
### 4. Run backend server
```bash
python run.py

or
python app.py

or python3 in some cases
```
### 5. Example dashboard
I have provided an example dashboard which you can access at:
```bash
http://localhost:8000
```
Please feel free to construct a Frontend that caters to your needs.

## Contributions
Issue discussions and pull requests are welcome! If you need to add a feature, extend pool support or improve performance please do so!

To add a custom monitor or source, edit `config/sources.json` i.e:
```bash
{
  "name": "Custom Monitor",
  "url": "added monitor url",
  "type": "custom",
  "mode": "ws"
}
```
## Remember

Always verify critical alerts through various sources before you take action on your own mining setup.
