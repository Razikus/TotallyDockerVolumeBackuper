import boto3

def pushArchive(spec, transferMethod, sharedObj):
    region_name = transferMethod.get("region_name", None)
    aws_access_key_id = transferMethod.get("aws_access_key_id", None)
    aws_secret_access_key = transferMethod.get("aws_secret_access_key", None)
    vault_name = transferMethod.get("vault_name", None)
    archivePath = spec["path"]
    if(not vault_name):
        print("[GLACIER FAIL] No vault name in config")
        return False

    glacier = boto3.client('glacier', region_name=region_name,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)
    object_data = open(archivePath, "rb")
    try:
        print("[GLACIER] Uploading...")
        archive = glacier.upload_archive(vaultName=vault_name, body=object_data)
        print(f"[GLACIER] Done! Archive id: {archive['archiveId']}")
    except Exception as e:
        print(e)
        return False
    finally:
        object_data.close()
    return True