
clean:
	find . -name __pycache__ -delete

docs: clean
	pdoc3 . --html --force -o docs; mv docs/private_ip_bridge/* docs; rm -rf docs/private_ip_bridge
