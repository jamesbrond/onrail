PACKAGE      := onrail
MAKE_DIR     = .make
DIST_DIR     = release
GIT_HOOKS_DIR= .git/hooks
VENV_DIR     = .venv

PYTHON       = /cygdrive/c/Users/320072283/bin/python/python.exe
VERSION_FILE = .version
# regexp (PRE)(VERSION)(POST)
VERSION_EXP  = ^( *)([0-9.]+)(.*)

PY_CONF_FLAKE8 = .lint/flake8
PY_CONF_PYLINT = .lint/pylint.toml

# define all directories to be created
# each included Makefile may add to $(DIRS)
DIRS = $(MAKE_DIR) $(DIST_DIR)

WEB_DIR  := web
WEB_OBJS := $(DIST_DIR)/cal.js $(DIST_DIR)/style.css

SHELL:=/bin/bash

-include $(MAKE_DIR)/misc.mk
-include $(MAKE_DIR)/git.mk
-include $(MAKE_DIR)/py.mk

# download all missing include Makefiles
$(MAKE_DIR)/%.mk: | $(MAKE_DIR)
	@URL=$$(echo "https://raw.githubusercontent.com/jamesbrond/jamesbrond/main/Makefile/.make/$(@F)"); \
	echo "get $$URL"; \
	curl -s -H 'Cache-Control: no-cache, no-store' $${URL} -o $@

.PHONY: build clean distclean dist init lint test
.DEFAULT_GOAL := help

$(DIRS):
	@$(call log-debug,MAKE,make '$@' folder)
	@mkdir -p $@

build:: ## Compile the entire program
	@$(call log-info,MAKE,$@ done)

clean:: ## Delete all files created by this makefile, however don’t delete the files that record configuration or environment
	@-$(RM) onrail.log
	@$(call log-info,MAKE,$@ done)

distclean:: clean ## Delete all files in the current directory (or created by this makefile) that are created by configuring or building the program
	@-$(RMDIR) $(BUILD_DIR) $(NULL_STDERR)
	@-$(RMDIR) $(DIST_DIR) $(NULL_STDERR)
	@-$(RMDIR) $(MAKE_DIR) $(NULL_STDERR)
	@$(call log-info,MAKE,$@ done)

dist:: build $(WEB_OBJS) $(DIST_DIR)/index.html ## Create a distribution file or files for this program
	@$(call log-info,MAKE,$@ done)

init:: ## Initialize development environment
	@yarn install
	@$(call log-info,MAKE,$@ done)

lint:: ## Perform static linting
	@$(call log-info,MAKE,$@ done)

test:: build ## Unit test
	@$(call log-info,MAKE,$@ done)

$(DIST_DIR)/index.html: | $(DIST_DIR)
	@$(call log-debug,MAKE,copy '$@' file)
	@cp $(WEB_DIR)/index.html $(DIST_DIR)

$(WEB_OBJS): | $(DIST_DIR)
	@$(call log-debug,MAKE,run webpack)
	@yarn webpack

xxx:
	@echo $(PY_SRCS)

# ~@:-]
