#!/usr/bin/env bash
# Fetch the public mdzip corpus used by check_mdzip.py.
# Files are third-party sample models; they are NOT committed to this repo.
# Destination: $MDZIP_CORPUS (default /tmp/mdzip_probe)
set -euo pipefail
DEST="${MDZIP_CORPUS:-/tmp/mdzip_probe}"
mkdir -p "$DEST"

fetch() {  # name url
    local name="$1" url="$2"
    if [ -s "$DEST/$name.mdzip" ]; then
        echo "have $name"
    else
        echo "fetching $name"
        curl -fsSL -o "$DEST/$name.mdzip" "$url"
    fi
}

# Open-MBEE OpenSE-Cookbook (master): APE reference model, 21 MB
fetch APE "https://raw.githubusercontent.com/Open-MBEE/OpenSE-Cookbook/master/Models/APE-ReferenceModel.mdzip"
# GaloisInc VERSE-OpenSUT (main): MPS instrumentation architecture (Cameo 2021x-era)
fetch MPS "https://media.githubusercontent.com/media/GaloisInc/VERSE-OpenSUT/main/models/SysMLv1/MPS.mdzip"
# autarchprinceps Multiagent-Warehouse (master): 2015-era MagicDraw file
fetch maas-warehouse "https://media.githubusercontent.com/media/autarchprinceps/Multiagent-Warehouse/master/Documentation/maas-warehouse.mdzip"

ls -la "$DEST"
echo "Run: MDZIP_CORPUS=$DEST python check_mdzip.py"