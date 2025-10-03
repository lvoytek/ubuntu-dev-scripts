#!/usr/bin/python3

"""Create an nginx profile and lxd proxy to send web requests from a domain to a container."""


import argparse
from os import system
from pathlib import Path

def create_lxd_proxy(container_name: str, host_port: int, container_port: int, debug: bool):
    """Use lxc config to add a new proxy for mapping a port to a container."""
    proxy_str = f"lxc config device add {container_name} {container_name}{host_port} proxy listen=tcp:0.0.0.0:{host_port} connect=tcp:127.0.0.1:{container_port}"

    if debug:
        print("Running %s", proxy_str)

    result = system(proxy_str)

    if result != 0:
        print("Proxy creation failed with exit code %d", result)


def get_path_to_nginx_profile(domain: str) -> Path:
    """Get a standardized path for the domain's nginx profile."""
    return Path("/etc/nginx/sites-available/", domain.replace(".", "-"))


def create_nginx_profile(domain: str, host_port: int, debug: bool):
    """Create a new nginx profile with the given domain that redirects to the host port."""

    profile_str = "server {\n" +\
                  "\tlisten 80;\n" +\
                  f"\tserver_name {domain};\n" +\
                  "\tlocation / {\n" +\
                  "\t\tproxy_set_header X-Forwarded-For ote_addr;\n" +\
                  "\t\tproxy_set_header Host tp_host;\n" +\
                  f'\t\tproxy_pass "http://127.0.0.1:{host_port}";\n' +\
                  "\t}\n" +\
                  "}\n"

    if debug:
        print("Nginx profile:\n%s", profile_str)

    file = get_path_to_nginx_profile(domain)
    file.write_text(profile_str, encoding='utf-8')


def activate_nginx_profile(domain: str, debug: bool):
    """Link nginx profile to sites-enabled and restart nginx."""

    profile_name = str(get_path_to_nginx_profile(domain))

    if debug:
        print("Linking %s to sites-enabled", profile_name)

    result = system(f"ln -s {profile_name} /etc/nginx/sites-enabled/")

    if result != 0:
        print("Failed to link to sites-enabled with exit code %d", result)
        return

    if debug:
        print("Restarting nginx.")

    result = system("systemctl restart nginx")
    if result != 0:
        print("Failed to restart nginx with exit code %d", result)


def main(domain: str, container_name: str, host_port: int, container_port: int, run_proxy: bool, run_nginx_profile: bool, run_nginx_activate, debug: bool):
    """Run the port forwarding and nginx site creation."""
    if run_proxy:
        create_lxd_proxy(container_name, host_port, container_port, debug)

    if run_nginx_profile:
        create_nginx_profile(domain, host_port, debug)

    if run_nginx_activate:
        activate_nginx_profile(domain, debug)


def launch():
    """Launch with arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "domain",
        nargs="?",
        help="The website domain for nginx to look for.",
    )

    parser.add_argument(
        "--container-name",
        dest="container_name",
        default="mycontainer",
        help="The name of the container to forward data to.",
    )

    parser.add_argument(
        "--host-port",
        dest="host_port",
        default=3000,
        type=int,
        help="The host port to redirect nginx data to lxd through.",
    )

    parser.add_argument(
        "--container-port",
        dest="container_port",
        default=80,
        type=int,
        help="The port to forward data to the container through.",
    )

    parser.add_argument(
        "--skip-create-proxy",
        dest="skip_create_proxy",
        action="store_true",
        help="Skip the lxd proxy creation.",
    )

    parser.add_argument(
        "--skip-create-nginx-profile",
        dest="skip_create_nginx_profile",
        action="store_true",
        help="Skip creating the nginx profile.",
    )

    parser.add_argument(
        "--activate-nginx-profile",
        dest="activate_nginx_profile",
        action="store_true",
        help="Activate the nginx profile after creation.",
    )

    parser.add_argument("-d", "--debug", action="store_true", help="debug output")

    args = parser.parse_args()
    main(args.domain, args.container_name, args.host_port, args.container_port, not args.skip_create_proxy, not args.skip_create_nginx_profile, args.activate_nginx_profile, args.debug)


if __name__ == "__main__":
    launch()