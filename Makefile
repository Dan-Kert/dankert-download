all: lazy-extractors dankert-download doc pypi-files
clean: clean-test clean-dist
clean-all: clean clean-cache
completions: completion-bash completion-fish completion-zsh
doc: README.md CONTRIBUTING.md CONTRIBUTORS issuetemplates supportedsites
ot: offlinetest
tar: dankert-download.tar.gz

pypi-files: AUTHORS Changelog.md LICENSE README.md README.txt supportedsites \
            completions dankert-download.1 pyproject.toml setup.cfg devscripts/* test/*

.PHONY: all clean clean-all clean-test clean-dist clean-cache \
        completions completion-bash completion-fish completion-zsh \
        doc issuetemplates supportedsites ot offlinetest codetest test \
        tar pypi-files lazy-extractors install uninstall

clean-test:
	rm -rf tmp/ *.annotations.xml *.aria2 *.description *.dump *.frag \
	*.frag.aria2 *.frag.urls *.info.json *.live_chat.json *.meta *.part* *.tmp *.temp *.unknown_video *.ytdl \
	*.3gp *.ape *.ass *.avi *.desktop *.f4v *.flac *.flv *.gif *.jpeg *.jpg *.lrc *.m4a *.m4v *.mhtml *.mkv *.mov *.mp3 *.mp4 \
	*.mpg *.mpga *.oga *.ogg *.opus *.png *.sbv *.srt *.ssa *.swf *.tt *.ttml *.url *.vtt *.wav *.webloc *.webm *.webp \
	test/testdata/sigs/player-*.js test/testdata/thumbnails/empty.webp "test/testdata/thumbnails/foo %d bar/foo_%d."*

clean-dist:
	rm -rf dankert-download.1.temp.md dankert-download.1 README.txt MANIFEST build/ dist/ .coverage cover/ dankert-download.tar.gz completions/ \
	dankert_install/extractor/lazy_extractors.py *.spec CONTRIBUTING.md.tmp dankert-download dankert-download.exe dankert_install.egg-info/ AUTHORS

clean-cache:
	find . \( \
		-type d -name ".*_cache" -o -type d -name __pycache__ -o -name "*.pyc" -o -name "*.class" \
	\) -prune -exec rm -rf {} \;

completion-bash: completions/bash/dankert-download
completion-fish: completions/fish/dankert-download.fish
completion-zsh: completions/zsh/_dankert-download
lazy-extractors: dankert_install/extractor/lazy_extractors.py

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin
MANDIR ?= $(PREFIX)/man
SHAREDIR ?= $(PREFIX)/share
PYTHON ?= /usr/bin/env python3
GNUTAR ?= tar

PANDOC_VERSION_CMD = pandoc -v 2>/dev/null | head -n1 | cut -d' ' -f2 | head -c1
PANDOC_VERSION != $(PANDOC_VERSION_CMD)
PANDOC_VERSION ?= $(shell $(PANDOC_VERSION_CMD))
MARKDOWN_CMD = if [ "$(PANDOC_VERSION)" = "1" -o "$(PANDOC_VERSION)" = "0" ]; then echo markdown; else echo markdown-smart; fi
MARKDOWN != $(MARKDOWN_CMD)
MARKDOWN ?= $(shell $(MARKDOWN_CMD))

install: lazy-extractors dankert-download dankert-download.1 completions
	mkdir -p $(DESTDIR)$(BINDIR)
	install -m755 dankert-download $(DESTDIR)$(BINDIR)/dankert-download
	mkdir -p $(DESTDIR)$(MANDIR)/man1
	install -m644 dankert-download.1 $(DESTDIR)$(MANDIR)/man1/dankert-download.1
	mkdir -p $(DESTDIR)$(SHAREDIR)/bash-completion/completions
	install -m644 completions/bash/dankert-download $(DESTDIR)$(SHAREDIR)/bash-completion/completions/dankert-download
	mkdir -p $(DESTDIR)$(SHAREDIR)/zsh/site-functions
	install -m644 completions/zsh/_dankert-download $(DESTDIR)$(SHAREDIR)/zsh/site-functions/_dankert-download
	mkdir -p $(DESTDIR)$(SHAREDIR)/fish/vendor_completions.d
	install -m644 completions/fish/dankert-download.fish $(DESTDIR)$(SHAREDIR)/fish/vendor_completions.d/dankert-download.fish

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/dankert-download
	rm -f $(DESTDIR)$(MANDIR)/man1/dankert-download.1
	rm -f $(DESTDIR)$(SHAREDIR)/bash-completion/completions/dankert-download
	rm -f $(DESTDIR)$(SHAREDIR)/zsh/site-functions/_dankert-download
	rm -f $(DESTDIR)$(SHAREDIR)/fish/vendor_completions.d/dankert-download.fish

codetest:
	ruff check .
	autopep8 --diff .

test:
	$(PYTHON) -m pytest -Werror
	$(MAKE) codetest

offlinetest: codetest
	$(PYTHON) -m pytest -Werror -m "not download"

CODE_FOLDERS_CMD = find dankert_install -type f -name '__init__.py' | sed 's,/__init__.py,,' | grep -v '/__' | sort
CODE_FOLDERS != $(CODE_FOLDERS_CMD)
CODE_FOLDERS ?= $(shell $(CODE_FOLDERS_CMD))
CODE_FILES_CMD = for f in $(CODE_FOLDERS) ; do echo "$$f" | sed 's,$$,/*.py,' ; done
CODE_FILES != $(CODE_FILES_CMD)
CODE_FILES ?= $(shell $(CODE_FILES_CMD))
dankert-download: $(CODE_FILES)
	mkdir -p zip
	for d in $(CODE_FOLDERS) ; do \
	  mkdir -p zip/$$d ;\
	  cp -pPR $$d/*.py zip/$$d/ ;\
	done
	(cd zip && touch -t 200001010101 $(CODE_FILES))
	mv zip/dankert_install/__main__.py zip/
	(cd zip && zip -q ../dankert-download $(CODE_FILES) __main__.py)
	rm -rf zip
	echo '#!$(PYTHON)' > dankert-download
	cat dankert-download.zip >> dankert-download
	rm dankert-download.zip
	chmod a+x dankert-download

README.md: $(CODE_FILES) devscripts/make_readme.py
	COLUMNS=80 $(PYTHON) dankert_install/__main__.py --ignore-config --help | $(PYTHON) devscripts/make_readme.py

CONTRIBUTING.md: README.md devscripts/make_contributing.py
	$(PYTHON) devscripts/make_contributing.py README.md CONTRIBUTING.md

issuetemplates: devscripts/make_issue_template.py .github/ISSUE_TEMPLATE_tmpl/*.yml dankert_install/version.py
	$(PYTHON) devscripts/make_issue_template.py .github/ISSUE_TEMPLATE_tmpl/*.yml .github/ISSUE_TEMPLATE/

supportedsites:
	$(PYTHON) devscripts/make_supportedsites.py supportedsites.md

README.txt: README.md
	pandoc -f $(MARKDOWN) -t plain README.md -o README.txt

dankert-download.1: README.md devscripts/prepare_manpage.py
	$(PYTHON) devscripts/prepare_manpage.py dankert-download.1.temp.md
	pandoc -s -f $(MARKDOWN) -t man dankert-download.1.temp.md -o dankert-download.1
	rm -f dankert-download.1.temp.md

completions/bash/dankert-download: $(CODE_FILES) devscripts/bash-completion.in
	mkdir -p completions/bash
	$(PYTHON) devscripts/bash-completion.py

completions/zsh/_dankert-download: $(CODE_FILES) devscripts/zsh-completion.in
	mkdir -p completions/zsh
	$(PYTHON) devscripts/zsh-completion.py

completions/fish/dankert-download.fish: $(CODE_FILES) devscripts/fish-completion.in
	mkdir -p completions/fish
	$(PYTHON) devscripts/fish-completion.py

_EXTRACTOR_FILES_CMD = find dankert_install/extractor -name '*.py' -and -not -name 'lazy_extractors.py'
_EXTRACTOR_FILES != $(_EXTRACTOR_FILES_CMD)
_EXTRACTOR_FILES ?= $(shell $(_EXTRACTOR_FILES_CMD))
dankert_install/extractor/lazy_extractors.py: devscripts/make_lazy_extractors.py devscripts/lazy_load_template.py $(_EXTRACTOR_FILES)
	$(PYTHON) devscripts/make_lazy_extractors.py $@

dankert-download.tar.gz: all
	@$(GNUTAR) -czf dankert-download.tar.gz --transform "s|^|dankert-download/|" --owner 0 --group 0 \
		--exclude '*.DS_Store' \
		--exclude '*.kate-swp' \
		--exclude '*.pyc' \
		--exclude '*.pyo' \
		--exclude '*~' \
		--exclude '__pycache__' \
		--exclude '.*_cache' \
		--exclude '.git' \
		-- \
		README.md supportedsites.md Changelog.md LICENSE \
		CONTRIBUTING.md Collaborators.md CONTRIBUTORS AUTHORS \
		Makefile dankert-download.1 README.txt completions .gitignore \
		setup.cfg dankert-download dankert_install pyproject.toml devscripts test

AUTHORS: Changelog.md
	@if [ -d '.git' ] && command -v git > /dev/null ; then \
	  echo 'Generating $@ from git commit history' ; \
	  git shortlog -s -n HEAD | cut -f2 | sort > $@ ; \
	fi

CONTRIBUTORS: Changelog.md
	@if [ -d '.git' ] && command -v git > /dev/null ; then \
	  echo 'Updating $@ from git commit history' ; \
	  $(PYTHON) devscripts/make_changelog.py -v -c > /dev/null ; \
	fi
