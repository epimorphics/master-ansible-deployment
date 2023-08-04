from ansible.module_utils._text import to_text
from ansible.errors import AnsibleFilterError
import boto3
from botocore.exceptions import ClientError

class FilterModule(object):
    def filters(self):
        return {
            'ec2_sgId': self.ec2_sgId
        }

    def ec2_sgId(self, secgrps, vpc):
        if vpc:
            try:
                response = boto3.client('ec2').describe_security_groups(Filters=[{'Name':'vpc-id','Values':[vpc]}])
                r = ''
                found = {}
                for sg in secgrps:
                    found[sg] = False
                if response['SecurityGroups']:
                    for g in response['SecurityGroups']:
                        for sg in secgrps:
                            if (g['GroupName']==sg):
                                if r:
                                    r = r + ',' + g['GroupId']
                                else:
                                    r = g['GroupId']
                                found[sg] = True
                    for sg in secgrps:
                        if not found[sg]: 
                            raise AnsibleFilterError('ec2_sgId: Security Group ({}) not found in {}'.format(sg, vpc))
                    return to_text(r)
                else:
                    raise AnsibleFilterError('ec2_sgId: No Security Groups for {}'.format(vpc))
            except ClientError as e:
                raise AnsibleFilterError('ec2_sgId: {}. Invalid vpc: {}'.format(e, vpc))

        else:
            raise AnsibleFilterError('ec2_sgId: VPC missing')
