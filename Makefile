.PHONY: check
check:
	@bad=$$(git ls-files | grep -E '(^|/)\.env(\.|$$)|\.(pem|key|p12)$$|(^|/)id_(rsa|ed25519)' | grep -v -E '\.(example|sample|template)$$' || true); \
	if [ -n "$$bad" ]; then echo "tracked secret-like files:"; echo "$$bad"; exit 1; fi; \
	if git grep -I -n -e 'BEGIN [A-Z ]*PRIVATE KEY' -- . ':!.github' ':!Makefile'; then echo "private key material is tracked"; exit 1; fi
