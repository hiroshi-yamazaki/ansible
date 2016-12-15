#!/usr/bin/python
#encoding: utf-8

# This task requires follow IAM Policies
# 
# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Effect": "Allow",
#             "Action": [
#                 "ec2:Describe*",
#                 "ec2:CreateSnapshot",
#                 "ec2:DeleteSnapshot",
#                 "ec2:CreateTags",
#                 "ec2:DeleteTags"
#             ],
#             "Resource": "*"
#         }
#     ]
# }

import boto.ec2

region = '{{ ec2.region }}'
aws_access_key = '{{ ec2.access_key }}'
aws_secret_key = '{{ ec2.secret_key }}'
tag_name = '{{ ec2.tag_name }}'

ec2 = boto.ec2.connect_to_region(region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
instances = [i for r in ec2.get_all_instances(filters={'tag:Name':tag_name, 'tag:backup':'ON'}) for i in r.instances]

for instance in instances:
  #print "backup instance: %s" % instance.id

  generation = int(instance.tags.get('generation'))
  #print "backup generation: %s" % generation

  volumes = ec2.get_all_volumes(filters={'attachment.instance-id': instance.id})

  for v in volumes:
    # 新しいsnapshotを作成する
    #print "create snapshot: %s" % v.id
    v.create_snapshot(description=tag_name + '-snapshot-' + v.id)

    # start_timeの降順で並び替え、古い世代のsnapshotを削除する
    snaps = v.snapshots()
    sorted_snaps = sorted(snaps, key=lambda snap: snap.start_time, reverse=True)
    for i, snap in enumerate(sorted_snaps):
      if i >= generation:
        #print "delete snapshot: %s" % snap.id
        snap.delete()
