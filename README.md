# News Site

## Deploy to aws with Zappa

[Set up your aws cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html):

```bash
pip install awscli
aws config
```

Set up your virtual environemnt:

```bash
pip install virtualenv
cd /project/dir
virtualenv --python=python3 venv
```

Deploy or update the site:

```bash
source venv/bin/activate
pip install -r requirements.txt
zappa deploy prod
zappa update prod
```

Deploy under your [Route53](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started.html) domain and [ACM](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html) cert:

Update these lines in zappa_settings.json:

```javascript
"domain": "themcilroy.com",
"certificate_arn": "arn:aws:acm:us-east-1:824269988929:certificate/a029b88f-a7f8-40a4-bd09-3a49787d4c73"
```

Deploy your cert (this takes awhile to propigate):
> zappa certify

Tear it all down with:
> zappa undeploy