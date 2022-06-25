from database.models import TblUserDevices


def check_device(user_id=None, device_model=None, imei_number=None):
    # print(f'raw device model ================== {device_model}')

    txt = device_model
    x = txt.find(":")  # 5
    y = txt.find(",")  # 11
    # print(f'device model ================================= {txt[x+2:y]}')
    try:
        obj = TblUserDevices.objects.filter(
            fld_user_id=user_id, fld_is_active=True, fld_device_model__icontains=txt[x+2:y]).last()
        # print(f'TblUserDevices ===================================== {obj}')
    except:
        obj = None
    if obj:
        return {"device": txt[x+2:y].lower()}
    return None
