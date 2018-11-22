#
# Overi ci NMEA veta a checksum sedia, vracia True, False
#
def NMEAchecksum(NMEA_veta):

    if NMEA_veta.count('*') != 1 and NMEA_veta[len(NMEA_veta)-3]:
        return False

    # ak je na zaciatku $ tak sa odstrani
    if NMEA_veta[0] == "$":
        NMEA_veta = NMEA_veta.replace('$','')

    return True
pass
