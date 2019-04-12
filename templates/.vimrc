" appearance
syntax enable
set number
set showcmd
set showmatch
set wildmenu

" behavior
noremap j gj
noremap k gk
inoremap jk <esc> 
set hlsearch
set incsearch
set lazyredraw
set directory=~/.vim/tmp
filetype plugin on

" indentation
set tabstop=4
set softtabstop=4
set shiftwidth=4
set expandtab
filetype indent on

" custom file types
autocmd FileType yaml,yml setlocal tabstop=2 softtabstop=2 shiftwidth=2
