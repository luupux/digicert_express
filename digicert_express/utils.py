import loggers
import platform
import re
import os

def normalize_common_name_file(common_name):
    return common_name.replace("*", "any").replace(".", "_")

def determine_platform():
    logger = loggers.get_logger(__name__)
    distro_name = platform.linux_distribution()  # returns a tuple ('', '', '') (distroName, version, code name)
    logger.debug("Found platform: {0}".format(" : ".join(distro_name)))
    return distro_name

def create_regex(text):
    """
    Escape and return the passed string in upper and lower case to match regardless of case.
    Augeas 1.0 supports the standard regex /i but previous versions do not.  Also, not all (but most) unix/linux
    platforms support /i.  So this is the safest method to ensure matches.

    :param text: string to create regex from
    :return: regex
    """

    return "".join(["[" + c.upper() + c.lower() + "]" if c.isalpha() else c for c in re.escape(text)])

def get_dns_names_from_cert(cert_path):
    command = "sudo openssl x509 -in {0} -text -noout | sed -nr '/^ {{12}}X509v3 Subject Alternative Name/{{n; s/(^|,) *DNS:/,/g; s/(^|,) [^,]*//g;p}}'".format(cert_path)
    dns_names_result = os.popen(command).read()
    dns_names = dns_names_result.split(',')
    dns_names = [x for x in dns_names if x]
    return dns_names