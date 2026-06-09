> **NOTE:** to use pdf build GitHub action, you might need to enable Write Access for our workflow.
> Navigate **Settings -> Actions -> General** and change **Workflow Permissions** to **Read and Write permissions**

<p align="center">
<!--AUTOURL-BEGIN-->
<a href="https://github.com/gucio321/FT2zXcXvX/blob/pdf/ft2zxcxvx.pdf">
<!--AUTOURL-END-->
<img src="./resources/button.png"></a>
</p>

# Description

Template for Physics Labs reports on AGH. -- Szablon sprawozdań z Laboratorium Fizycznego AGH.

## Usage

1. Clone this repository or create your own from the template.
2. Edit `conf.py` and/or other files (I'll put list here). The variables you may want to use are on top of `conf.py` (title/author, e.t.c.)
3. (Only first time) Generate virtual enviroument `uv venv`
4. Activate venv `source .venv/bin/activate`
5. (Only first time) Install dependencies `uv sync`
5. Edit `assets/document.md` and/or other files
6. Use makefile to generate project (`make html` / `make latexpdf`)

<details><summary>Pre requirements</summary>

- On fedora you need to install this:

```sh
dnf install -y latexmk texlive-cmap texlive-collection-fontsrecommended texlive-fncychap texlive-wrapfig texlive-capt-of texlive-framed texlive-upquote texlive-needspace texlive-tabulary texlive-parskip texlive-oberdiek texlive-cancel texlive-hyphen-polish texlive-pict2e texlive-ellipse.noarch
```

- on `apt`-based linux:

```sh
sudo apt install -y latexmk texlive texlive-fonts-extra texlive-full texlive-lang-polish
```

- on other distros: Generally you need to find the following:
    * `pdflatex` command
    * something like `texlive-full`
    * polish babel version (e.g. search for `texlive*polish*`)

- On windows: STOP USEING WINDOWS. Ok, seriously speaking: check out the previous point - you need same setup.

</details>

Available technologies:
- Markdown files support
- Latex formulas
- Plots [check here for more info](https://pypi.org/project/sphinxcontrib-plot/)

## Resources

- [AGH - WFIiS Title Pag template](https://www.overleaf.com/latex/templates/praca-dyplomowa/kbwcrcmczypy)
