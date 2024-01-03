PACKAGE      := onrail
BUILD_DIR    = build
MAKE_DIR     = $(BUILD_DIR)/make
DIST_DIR     = release
GIT_HOOKS_DIR= .git/hooks
VENV_DIR     = $(BUILD_DIR)/venv
WEB_DIR      := src/web

PYTHON       = /cygdrive/c/Users/320072283/bin/python/python.exe
VERSION_FILE = .version
# regexp (PRE)(VERSION)(POST)
VERSION_EXP  = ^( *)([0-9.]+)(.*)

PY_CONF_FLAKE8 = .flake8
PY_CONF_PYLINT = .pylint.toml

# define all directories to be created
# each included Makefile may add to $(DIRS)
DIRS = $(MAKE_DIR) $(DIST_DIR)

SHELL:=/bin/bash

-include $(MAKE_DIR)/misc.mk
-include $(MAKE_DIR)/git.mk
-include $(MAKE_DIR)/py.mk

WEBPACK_CONF = $(wildcard webpack.config.js)
WEB_SRCS := $(WEB_DIR)/index.js $(WEB_DIR)/style.scss
DEV_WEB_OBJS := $(BUILD_DIR)/web/cal.js
DEV_PY_OBJS  := $(patsubst src/%,$(BUILD_DIR)/%,$(PY_SRCS))
PROD_WEB_OBJS := $(DIST_DIR)/web/cal.js
PROD_PY_OBJS  := $(patsubst src/%,$(DIST_DIR)/%,$(PY_SRCS))


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

build:: $(DEV_PY_OBJS) $(DEV_WEB_OBJS) $(BUILD_DIR)/web/index.html ## Compile the entire program
	@$(call log-info,MAKE,$@ done)

clean:: ## Delete all files created by this makefile, however don’t delete the files that record configuration or environment
	@-$(RM) onrail.log
	@$(call log-info,MAKE,$@ done)

distclean:: clean ## Delete all files in the current directory (or created by this makefile) that are created by configuring or building the program
	@-$(RMDIR) $(BUILD_DIR) $(NULL_STDERR)
	@-$(RMDIR) $(DIST_DIR) $(NULL_STDERR)
	@-$(RMDIR) $(MAKE_DIR) $(NULL_STDERR)
	@$(call log-info,MAKE,$@ done)

dist:: $(PROD_PY_OBJS) $(PROD_WEB_OBJS) $(DIST_DIR)/web/index.html ## Create a distribution file or files for this program
	@$(call log-info,MAKE,$@ done)

init:: ## Initialize development environment
	@yarn install
	@$(call log-info,MAKE,$@ done)

lint:: ## Perform static linting
	@$(call log-info,MAKE,$@ done)

test:: build ## Unit test
	@$(call log-info,MAKE,$@ done)

$(BUILD_DIR)/%: src/%
	@$(call log-debug,MAKE,Copy source '$@' to '$(BUILD_DIR)/')
	@mkdir -p $(@D) && cp -rf $< $@

$(DIST_DIR)/%: src/%
	@$(call log-debug,MAKE,Copy source '$@' to '$(DIST_DIR)/')
	@mkdir -p $(@D) && cp -rf $< $@

$(DEV_WEB_OBJS): $(WEBPACK_CONF) $(WEB_SRCS) | $(BUILD_DIR)
	@$(call log-debug,MAKE,run webpack development mode)
	@yarn webpack build --config $(WEBPACK_CONF) --output-path $(BUILD_DIR)/web --mode="development"

$(PROD_WEB_OBJS): $(WEBPACK_CONF) $(WEB_SRCS) | $(DIST_DIR)
	@$(call log-debug,MAKE,run webpack production mode)
	@yarn webpack build --config $(WEBPACK_CONF) --output-path $(DIST_DIR)/web --mode="production"


# ~@:-]
