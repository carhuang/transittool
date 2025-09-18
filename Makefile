BINDIR = $(HOME)/.local/bin
TARGET = $(BINDIR)/transittool
SRC = $(PWD)/transittool

.PHONY: install uninstall test

install:
	@mkdir -p $(BINDIR)
	@ln -sf $(SRC) $(TARGET)
	@echo "Installed symlink: $(TARGET) -> $(SRC)"

uninstall:
	@rm -f $(TARGET)
	@echo "Removed symlink: $(TARGET)"

test:
	@python3 -m pytest -q