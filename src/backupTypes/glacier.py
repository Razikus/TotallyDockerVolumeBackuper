import boto3

def pushArchive(archivePath):
    glacier = boto3.client('glacier', region_name="eu-central-1",
    aws_access_key_id='XXXXXX',
    aws_secret_access_key='XXXXXXXXXXX')
    vault_name = "s1-backups"
    object_data = open(archivePath, "rb")
    try:
        print("[GLACIER] Uploading...")
        archive = glacier.upload_archive(vaultName=vault_name, body=object_data)
        print(f"[GLACIER] Done! Archive id: {archive['archiveId']}")
    except ClientError as e:
        print(e)
        logging.error(e)
        return None
    finally:
        object_data.close()
    return True