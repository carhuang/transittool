BINDIR = $(HOME)/.local/bin
TARGET = $(BINDIR)/transittool
SRC = $(PWD)/transittool
VENV = .venv

.PHONY: install uninstall venv test

install:
	@mkdir -p $(BINDIR)
	@ln -sf $(SRC) $(TARGET)
	@echo "Installed symlink: $(TARGET) -> $(SRC)"

uninstall:
	@rm -f $(TARGET)
	@echo "Removed symlink: $(TARGET)"

venv:
	@if [ -x "$(VENV)/bin/python" ]; then \
        echo "Using existing venv at $(VENV)"; \
	else \
			python3 -m venv $(VENV); \
			$(VENV)/bin/python -m pip install -U pip setuptools wheel; \
			$(VENV)/bin/python -m pip install -r requirements-dev.txt 2>/dev/null || true; \
	fi

test: venv
	$(VENV)/bin/python3.10 -m pytest -q