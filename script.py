import boto3

client = boto3.client('ecr', region_name='eu-west-1')
paginator = client.get_paginator('describe_repositories')
response_iterator = paginator.paginate()

repoNames = []
maxResults = 1000


def getRepos():
    for page in response_iterator:
        for repo in page['repositories']:  # Iterate over every dict element of the list of dict.
            repoNames.append(repo['repositoryName'])  # Add the repo name to a list so we can iterate over them later.

        repoNames.sort()  # Sort alphabetically.
        print("Total Number of ECR repositories: " + str(len(repoNames)))


def listImages():
    # Iterate over every repo we found earlier.
    for repo in repoNames:
        # List the images for a repo.
        images = client.list_images(repositoryName=repo, maxResults=maxResults)
        imagesCount = []
        sha = []

        # For every imageIds, find unique images only.

        for d in images['imageIds']:
            if d['imageDigest'] not in sha:
                sha.append((d['imageDigest']))  # Add only unique images to a list
        imagesCount.append((len(sha)))  # Count the number of unique images for a repo.

        # make another call with the nextToken if more than 1000 results are returned.
        while len(images['imageIds']) == maxResults:
            images = client.list_images(repositoryName=repo, maxResults=1000, nextToken=images['nextToken'])
            sha = []
            for d in images['imageIds']:
                if d['imageDigest'] not in sha:
                    sha.append((d['imageDigest']))
            imagesCount.append((len(sha)))  # add the number of images in the repo to the list.

        print(repo + ": " + str(sum(imagesCount)))


getRepos()
listImages()
