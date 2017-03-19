#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys


def log_debug(cfg, msg):
    """Debug log"""
    if cfg.getboolean('DEFAULT', 'debug'):
        print(msg)


def asterisk_pjsip_user_config(cfg, phonenum, username, userpass, pickupgroup):
    """generate sip user config for Asterisk"""
    log_debug(cfg,
        "called func asterisk_pjsip_user_config({}, {}, {}, {}, {})".format(
            "cfg",
            phonenum,
            username,
            userpass,
            pickupgroup))
    log_debug(cfg, "Generating PJSIP config for {} {}".format(
        phonenum, username))
    user_config = "; AUTOGENERATED, do not modify manually\n"
    user_config += "; {} <{}> {}\n".format(phonenum, username, userpass)
    user_config += "\n\n"
    user_config += "[{}]\n".format(phonenum)
    user_config += "type=auth\n"
    user_config += "auth_type=userpass\n"
    user_config += "username={}\n".format(phonenum)
    user_config += "password={}\n".format(userpass)
    user_config += "\n"
    user_config += "[{}]\n".format(phonenum)
    user_config += "type=aor\n"
    user_config += "max_contacts=1\n"
    user_config += "remove_existing=yes\n"
    user_config += "qualify_frequency=5\n"
    user_config += "\n"
    user_config += "[{}]\n".format(phonenum)
    user_config += "type=endpoint\n"
    user_config += "callerid={} <{}>\n".format(username, phonenum)
    user_config += "transport={}\n".format(
        cfg.get('asterisk', 'pjsip_transport'))
    user_config += "context={}\n".format(cfg.get('asterisk', 'user_context'))
    user_config += "disallow=all\n"
    user_config += "allow={}\n".format(cfg.get('asterisk', 'codecs_allow'))
    user_config += "aors={}\n".format(phonenum)
    user_config += "auth={}\n".format(phonenum)
    user_config += "rtp_symmetric=yes\n"
    user_config += "rtp_ipv6=yes\n"
    user_config += "rewrite_contact=yes\n"
    user_config += "send_rpid=yes\n"
    user_config += "named_call_group={}\n".format(pickupgroup)
    user_config += "named_pickup_group={}\n".format(pickupgroup)
    user_config += "tos_audio=ef\n"
    user_config += "cos_audio=5\n"
    user_config += "\n"
    log_debug(cfg, user_config)
    return user_config


def asterisk_sip_user_config(cfg, phonenum, username, userpass, pickupgroup):
    """generate sip user config for Asterisk"""
    log_debug(cfg, "called func asterisk_sip_user_config({}, {})".format(
        phonenum,
        username))
    log_debug(cfg, "Generating SIP config for {} {}".format(
        phonenum, username))
    user_config = "; AUTOGENERATED, do not modify manually\n"
    user_config += "; {} <{}> {}\n\n".format(phonenum, username, userpass)
    user_config += "[{}]\n".format(phonenum)
    user_config += "type=friend\n"
    user_config += "host=dynamic\n"
    user_config += "username={}\n".format(phonenum)
    user_config += "secret={}\n".format(userpass)
    user_config += "fullname={}\n".format(phonenum)
    user_config += "callerid={}\n".format(username)
    user_config += "context={}\n".format(cfg.get('asterisk', 'user_context'))
    user_config += "transport=udp\n"
    user_config += "disallow=all\n"
    user_config += "allow={}\n".format(cfg.get('asterisk', 'codecs_allow'))
    user_config += "canreinvite=no\n"
    user_config += "nat=yes\n"
    user_config += "qualify=yes\n"
    user_config += "hassip=yes\n"
    user_config += "hasiax=no\n"
    user_config += "hash323=no\n"
    user_config += "hasmanager=no\n"
    user_config += "namedcallgroup={}\n".format(pickupgroup)
    user_config += "namedpickupgroup={}\n".format(pickupgroup)
    user_config += "\n"
    log_debug(cfg, user_config)
    return user_config


def yealink_phone_config(
        cfg, phonetype, phonehwmac, phonenum, username, userpass):
    """generate and write phone cfg file"""
    log_debug(cfg, "called func yealink_phone_config({}, {}, {}, {})".format(
        phonetype,
        phonehwmac,
        phonenum,
        username))
    # vars
    qos_rtptos = 46
    qos_signaltos = 26
    # CFG
    if phonetype == "1" or phonetype == "2":
        cfgdata = ""
        # Account section
        cfgdata += "[ account ]\n"
        cfgdata += "path = /config/voip/sipAccount0.cfg\n"
        cfgdata += "Enable = 1\n"
        cfgdata += "Label = " + str(phonenum) + " - " + str(username) + "\n"
        cfgdata += "DisplayName = " + str(phonenum) + "\n"
        cfgdata += "AuthName = " + str(phonenum) + "\n"
        cfgdata += "UserName = " + str(phonenum) + "\n"
        cfgdata += "password = " + userpass + "\n"
        cfgdata += "SIPServerHost = {}\n".format(
            cfg.get('asterisk', 'server_address'))
        cfgdata += "SIPServerPort = 5060\n"
        cfgdata += "Transport = 0\n"
        cfgdata += "\n"
        # Local Time section
        cfgdata += "[ LocalTime ]\n"
        cfgdata += "path = /config/Network/Network.cfg\n"
        cfgdata += "local_time.time_zone = {}\n".format(
            cfg.get('yealink', 'time_zone'))
        cfgdata += "local_time.summer_time = {}\n".format(
            cfg.get('yealink', 'summer_time'))
        cfgdata += "\n"
        # Network section
        cfgdata += "[ Network ]\n"
        cfgdata += "path = /config/Network/Network.cfg\n"
        cfgdata += "eWANType = 2\n"
        cfgdata += "\n"
        # LLDP section
        cfgdata += "[ LLDP ]\n"
        cfgdata += "path = /config/Network/Network.cfg\n"
        cfgdata += "EnableLLDP = 1\n"
        cfgdata += "\n"
        # QOS section
        cfgdata += "[ QOS ]\n"
        cfgdata += "path = /config/Network/Network.cfg\n"
        cfgdata += "RTPTOS = {}\n".format(qos_rtptos)
        cfgdata += "SIGNALTOS = {}\n".format(qos_signaltos)
        cfgdata += "\n"
        # Security section
        cfgdata += "[ AdminPassword ]\n"
        cfgdata += "path = /config/Setting/autop.cfg\n"
        cfgdata += "password = {}\n".format(
            cfg.get('yealink', 'admin_pass'))
        cfgdata += "\n"
        # End of config
        log_debug(cfg, "Generating phone config: ")
        log_debug(cfg, "phonetype: " + phonetype)
        log_debug(cfg, "phonehwmac: " + phonehwmac)
        log_debug(cfg, "phonenum: " + phonenum)
        log_debug(cfg, "username: " + username)
    elif phonetype == "5":
        cfgdata = "#!version:1.0.0.1\n"
        # Account section
        cfgdata += "account.1.enable = 1\n"
        cfgdata += "account.1.label = {}-{}\n".format(
            str(phonenum),
            str(username))
        cfgdata += "account.1.display_name = {}\n".format(str(phonenum))
        cfgdata += "account.1.auth_name = {}\n".format(str(phonenum))
        cfgdata += "account.1.user_name = {}\n".format(str(phonenum))
        cfgdata += "account.1.password = {}\n".format(userpass)
        cfgdata += "account.1.sip_server.1.address = {}\n".format(
            cfg.get('asterisk', 'server_address'))
        cfgdata += "account.1.sip_server.1.port = 5060\n"
        cfgdata += "\n"
        # Local Time section
        cfgdata += "local_time.time_zone = {}\n".format(
            cfg.get('yealink', 'time_zone'))
        cfgdata += "local_time.summer_time = {}\n".format(
            cfg.get('yealink', 'summer_time'))
        cfgdata += "\n"
        # Network section
        cfgdata += "network.ip_address_mode = 2\n"
        cfgdata += "\n"
        # LLDP section
        cfgdata += "network.lldp.enable = 1\n"
        cfgdata += "\n"
        # QOS section
        cfgdata += "network.qos.rtptos = {}\n".format(qos_rtptos)
        cfgdata += "network.qos.signaltos = {}\n".format(qos_signaltos)
        cfgdata += "\n"
        # Security section
        cfgdata += "security.user_password = {}\n".format(
            cfg.get('yealink', 'admin_pass'))
        cfgdata += "\n"
        # End of config
        log_debug(cfg, "Generating phone config: ")
        log_debug(cfg, "phonetype: " + phonetype)
        log_debug(cfg, "phonehwmac: " + phonehwmac)
        log_debug(cfg, "phonenum: " + phonenum)
        log_debug(cfg, "username: " + username)
    else:
        print("Unknown phone type")
        sys.exit(1)
    log_debug(cfg, cfgdata)
    return cfgdata


# EOF
