#!/usr/bin/env bash
set -x
set -ue -o posix -o pipefail

make_pdf_in_dir () {
  local dir_name="${1}"
  cd "${dir_name}"
  time latexmk -pdf *-answer.tex *-task.tex || true
  cd -
}

make_pdf_all () {
  make_pdf_in_dir school-554/generated-2018-19
  make_pdf_in_dir school-554/generated-2019-20
  make_pdf_in_dir school-554/generated-2020-21
}

make_pdf_all
