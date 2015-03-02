# Add local node modules to path
export PATH:=$(shell pwd)/node_modules/.bin:$(PATH)

# Find various build tools. Allow each of these to be overridden on the command
# line.
LESSC?=$(shell PATH="$(PATH)" which lessc)
JEKYLL?=$(shell PATH="$(PATH)" which jekyll)
UGLIFY?=$(shell PATH="$(PATH)" which uglify)

# The "name" of this site. Usually exposed as <filetype>/<sitename>.<ext>
# files.
SITENAME:=clean-blog

# Alert user if could not find utilities.
ifeq ($(LESSC),)
$(error could not locate lessc utility)
endif
ifeq ($(JEKYLL),)
$(error could not locate jekyll utility)
endif
ifeq ($(UGLIFY),)
$(error could not locate uglify utility)
endif

# Specify all generated files
GENERATED_CSS:=css/$(SITENAME).css css/$(SITENAME).min.css
GENERATED_JS:=js/$(SITENAME).min.js js/jquery.min.js js/bootstrap.min.js
GENERATED_FILES:=$(GENERATED_CSS) $(GENERATED_JS)

.PHONY: all
all: site

.PHONY: clean
clean:
	rm -f $(GENERATED_FILES)

# Jekyll targets
.PHONY: site serve
JEKYKLL_DEPS:=$(GENERATED_CSS) $(GENERATED_JS)
site: $(JEKYKLL_DEPS)
	$(JEKYLL) build
serve: $(JEKYKLL_DEPS)
	$(JEKYLL) serve --watch --drafts

# Compile less/... stylesheets to css/...
css/%.css: less/%.less $(wildcard less/*.less)
	$(LESSC) "$<" "$@"
css/%.min.css: less/%.less $(wildcard less/*.less)
	$(LESSC) "$<" "$@" --clean-css="--s1 --advanced"

# Compute js/... scripts to js/....min.js
# Note: the horrible-ness which is join_with_commas is due to the perfect storm
# of make and uglify being wrong. make is wrong because it doesn't have a clean
# way to map "a b c d" into "a,b,c,d" and uglify is wrong because it wants its
# input files to be comma-separated.
comma = ,
join_with_commas = $(subst $(eval) ,$(comma),$1)
js/%.min.js: js/%.js
	$(UGLIFY) -s $(call join_with_commas,$^) -o "$@"
