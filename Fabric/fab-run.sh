#!/bin/bash
set -e

# cd /Users/euiyoung.hwang/ES/Python_Workspace/python-django
SCRIPTDIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

cd $SCRIPTDIR/basic

fab dev:user="euiyoung.hwang",services="update_rest_service"
# fab staging:user="euiyoung.hwang",services="update_rest_service"