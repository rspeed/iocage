"""activate module for the cli."""
import click
import libzfs

import iocage.lib.ioc_common as ioc_common

__rootcmd__ = True


@click.command(name="activate", help="Set a zpool active for iocage usage.")
@click.argument("zpool")
def cli(zpool):
    """Calls ZFS set to change the property org.freebsd.ioc:active to yes."""
    zfs = libzfs.ZFS(history=True, history_prefix="<iocage>")
    pools = zfs.pools
    prop = "org.freebsd.ioc:active"

    for _pool in pools:
        if _pool.name == zpool:
            ds = zfs.get_dataset(_pool.name)
            ds.properties[prop] = libzfs.ZFSUserProperty("yes")
        else:
            ds = zfs.get_dataset(_pool.name)
            ds.properties[prop] = libzfs.ZFSUserProperty("no")

        # Check and clean if necessary iocage_legacy way
        # to mark a ZFS pool as usable (now replaced by ZFS property)
        comment = zfs.get(_pool.name).properties["comment"]

        if comment.value == "iocage":
            comment.value = "-"

    ioc_common.logit({
        "level"  : "INFO",
        "message": f"ZFS pool '{zpool}' successfully activated."
    })
