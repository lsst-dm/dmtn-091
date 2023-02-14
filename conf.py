"""Sphinx configuration.
To learn more about the Sphinx configuration for technotes, and how to
customize it, see:
https://documenteer.lsst.io/technotes/configuration.html
"""

from documenteer.conf.technote import *  # noqa: F401, F403

# Ingest settings from metadata.yaml and use documenteer's configure_technote()
# to build a Sphinx configuration that is injected into this script's global
# namespace.
metadata_path = os.path.join(os.path.dirname(__file__), 'metadata.yaml')
with open(metadata_path, 'r') as f:
    confs = configure_technote(f)
g = globals()
g.update(confs)
