#!/bin/bash
remote="simm@home:~/home/"

scp *.sh $remote
scp -r org $remote
ssh simm@home "cd home; ./restart.sh"
