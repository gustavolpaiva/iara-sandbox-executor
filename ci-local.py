#!/usr/bin/env python3
"""CI determinístico, só stdlib, sem rede; executado na raiz do sandbox."""
from pathlib import Path
import sys


def main():
    raiz = Path(__file__).resolve().parent
    if (raiz / 'docs/FALHAR_CI').exists():
        print('CI-LOCAL FALHOU: controle negativo sintético')
        return 1
    arquivos = sorted((raiz / 'docs').rglob('*'))
    for p in arquivos:
        if p.is_symlink() or (not p.is_dir() and not p.is_file()):
            print('CI-LOCAL FALHOU: tipo de arquivo')
            return 1
        if p.is_file():
            try:
                dados = p.read_bytes()
                dados.decode('utf-8')
                if len(dados) > 262144 or b'\0' in dados:
                    raise ValueError()
            except (UnicodeError, ValueError):
                print('CI-LOCAL FALHOU: texto inválido')
                return 1
    print('CI-LOCAL PASSOU: texto sintético UTF-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
