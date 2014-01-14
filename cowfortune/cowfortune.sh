#!/bin/bash
cowsay -f `cowsay -l | tail -n +2 | tr " " "\\n" | sort -R | head -n1` `fortune`
