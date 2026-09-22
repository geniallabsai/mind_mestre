#!/usr/bin/env bash
# Remove o comando global e a pasta do mindmestre. O seu código não é tocado.
set -u
rm -f "$HOME/.local/bin/mindmestre" && echo "removido: ~/.local/bin/mindmestre"
rm -rf "$HOME/.genial-mind-mestre" && echo "removido: ~/.genial-mind-mestre"
echo "Genial Labs · MIND MESTRE removido. As saídas geradas (pasta ./saida) continuam onde estão."
