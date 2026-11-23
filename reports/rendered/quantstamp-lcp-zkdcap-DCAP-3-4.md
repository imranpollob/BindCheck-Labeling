# Quantstamp, Datachain LCP-zkDCAP (2025-03-03 to 2025-03-27), DCAP-3 and DCAP-4
Source: https://certificate.quantstamp.com/full/datachain-lcp-zk-dcap/15bac7cd-3b90-47c7-a25e-b0c3214c6630/index.html (rendered in Chrome 2026-11-23)

Report context (summary): DCAP attestation is verified through Risc0 zkVM, with the resulting ZK proof validated on-chain by the LCPClientZKDCAP contract. Scope: zkdcap crates (quote-verifier, types, zkvm/risc0 guest) and lcp-solidity contract diffs. Operational considerations: "The zkVM proof assumes that the provided Intel root certificate is trustworthy. The client should verify that the Intel root certificate from the proof's output is trusted." Privileged actor: operator; LCP client can require a threshold of enclave keys mapped to operators.

## DCAP-3 Missing Strict Validation of Critical x.509 Certificate Extensions (Low, Fixed)
Fixed in 80cc77a92d597d163621e887a01ecc599f41c259 ("introducing the validate_cert_extensions() function and applying it to the corresponding certificates").
File(s) affected: crates/quote-verifier/src/pck.rs, crates/quote-verifier/src/tcb_info.rs

Description: The current implementation of Intel SGX PCK certificate validation logic does not explicitly verify critical X.509 extensions such as Key Usage (OID: 2.5.29.15) and Basic Constraints (OID: 2.5.29.19). According to RFC5280 section 4.2, a certificate-using system must reject a certificate if it encounters a critical extension it does not recognize or a critical extension that contains information it cannot process. According to the Intel SGX PCK Certificate specification, certificates have the following extensions marked as "critical": PCK Leaf (KU DigitalSignature, NonRepudiation; CA:FALSE), PCK Issuer CA (KU CertSign, CRLSign; CA:TRUE pathlen:0), Intel SGX Root CA (KU CertSign, CRLSign; CA:TRUE pathlen:1), TCB Signing (KU DigitalSignature, NonRepudiation; CA:FALSE).

Failing to enforce these validations may allow certificates with inappropriate key usage or incorrect CA constraints, weakening the trustworthiness of the certificate chain.

Exploit Scenario: An attacker obtains or generates a rogue certificate incorrectly marked with CA:TRUE or with inappropriate Key Usage. If the validation logic fails to explicitly check these critical attributes, the system might incorrectly accept this certificate, potentially allowing it to sign or validate unauthorized certificates or CRLs, undermining the entire trust model.

Recommendation: Verify the presence and correctness of critical Key Usage and Basic Constraints extensions in all certificates (pck.rs::validate_pck_cert(): leaf, issuer, root; tcb_info.rs::validate_tcb_signing_certificate()). [sample code omitted]

## DCAP-4 Chain Validation Against Common Name and Not Distinguished Name (Low, Fixed)
Fixed in 309d1e48d8 ("added a check against the DN, verifying most fields against hardcoded and shared Intel values").
File(s) affected: crates/quote-verifier/src/pck.rs

Description: The validate_pck_cert() function currently relies on the Common Name (CN) to match certificates within the chain. This approach introduces potential security risks, as the CN alone is neither unique nor sufficient to unambiguously identify a certificate. Matching solely on CN can result in ambiguity and open the door to certain attacks, such as an adversary creating a certificate with the same CN as a trusted one. According to RFC 5280, section 4.1.2.4, the Distinguished Name (DN) should be used instead. [RFC quote omitted]

That said, we assess the risk to be low in this context, as the certificate must be signed by a trusted root certificate and SGX DCAP use cases are limited. As a result, it is unlikely that an attacker could successfully generate a PCK certificate with a colliding CN.

Exploit Scenario: An attacker could create a malicious certificate with the same CN as a trusted certificate. If the validate_pck_cert() function relies only on CN for matching, it might incorrectly trust the malicious certificate, leading to potential security breaches.

Recommendation: Update the certificate validation logic to compare the full DN for both the subject and the issuer rather than only the CN.
