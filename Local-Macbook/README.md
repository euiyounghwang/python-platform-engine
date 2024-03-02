
# Local Environment on Mac

- Install local tools
```bash
# homebrew
brew -v 

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# oh-my-zsh
brew install curl
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```


- Install aws configuration
```bash

# aws
brew install awscli
# source '/opt/homebrew/share/zsh/site-functions/_aws' >> ~/.zshrc


aws configure

# AWS Access Key ID [None]: aws cli 액세스 iam key
# AWS Secret Access Key [None]: aws cli 액세스 iam secret
# Default region name [None]: ap-northeast-2
# Default output format [None]: json

cat ~/.aws/credentials

# [default]
# aws_access_key_id = aws cli 액세스 iam key
# aws_secret_access_key = aws cli 액세스 iam secret

cat ~/.aws/config

# [default]
# region = ap-northeast-2
# output = json
```