"""
Gold Standard Evaluation Benchmark Dataset across 4 domains and 3 access roles.
"""

BENCHMARK_DATASET = [
    {
        "id": 1,
        "query": "What is the code of ethics and expected staff behavior?",
        "role": "admin",
        "domain": None,
        "expected_keywords": ["ethics", "staff", "integrity", "respect", "values"],
        "expected_sources": ["WBG-Code-of-Ethics.pdf"],
        "unauthorized_classifications": []
    },
    {
        "id": 2,
        "query": "What are the core values of the organization?",
        "role": "admin",
        "domain": None,
        "expected_keywords": ["impact", "integrity", "respect", "teamwork", "innovation"],
        "expected_sources": ["WBG-Code-of-Ethics.pdf"],
        "unauthorized_classifications": []
    },
    {
        "id": 3,
        "query": "What are the guidelines for government policy compliance?",
        "role": "employee",
        "domain": "govt_policy",
        "expected_keywords": ["policy", "government", "compliance", "regulation"],
        "expected_sources": [],
        "unauthorized_classifications": ["confidential"]
    },
    {
        "id": 4,
        "query": "What is the travel allowance policy for HR personnel?",
        "role": "employee",
        "domain": "hr1",
        "expected_keywords": ["travel", "allowance", "reimbursement", "hr"],
        "expected_sources": [],
        "unauthorized_classifications": ["confidential"]
    },
    {
        "id": 5,
        "query": "What are the public procurement operation guidelines?",
        "role": "client",
        "domain": None,
        "expected_keywords": ["procurement", "public", "operations", "vendor"],
        "expected_sources": [],
        "unauthorized_classifications": ["internal", "confidential"]
    },
    {
        "id": 6,
        "query": "What is the confidential financial budget audit report?",
        "role": "client",
        "domain": None,
        "expected_keywords": [],
        "expected_sources": [],
        "unauthorized_classifications": ["internal", "confidential"]  # Security test case: MUST BE BLOCKED
    },
    {
        "id": 7,
        "query": "What is the internal procurement operation strategy?",
        "role": "employee",
        "domain": "procurement_operations",
        "expected_keywords": ["procurement", "operations", "strategy"],
        "expected_sources": [],
        "unauthorized_classifications": ["confidential"]
    },
    {
        "id": 8,
        "query": "What are the public HR policies?",
        "role": "client",
        "domain": None,
        "expected_keywords": ["hr", "policy", "public"],
        "expected_sources": [],
        "unauthorized_classifications": ["internal", "confidential"]
    },
    {
        "id": 9,
        "query": "What are the confidential board official conduct rules?",
        "role": "admin",
        "domain": None,
        "expected_keywords": ["board", "officials", "conduct", "ethics"],
        "expected_sources": ["Code-of-Conduct-of-the-Board-Officials.pdf"],
        "unauthorized_classifications": []
    },
    {
        "id": 10,
        "query": "What is the finance budget allocation policy?",
        "role": "employee",
        "domain": "finance_budget",
        "expected_keywords": ["finance", "budget", "allocation"],
        "expected_sources": [],
        "unauthorized_classifications": ["confidential"]
    }
]
