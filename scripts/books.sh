#!/usr/bin/env bash
set -x
set -ue -o posix -o pipefail

install_packages () {
    brew install imagemagick
    brew upgrade imagemagick
    brew install ghostscript
}

downloadOld () {
  H='User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'
files='
5d1dd5c32f6185d1dd5c32f658.pdf
5d1dd52784f935d1dd52784fd3.pdf
5d14b2ab5e7255d14b2ab5e764.pdf
5d14b25bb47e55d14b25bb4825.pdf
5d14b1e3bd5d85d14b1e3bd618.pdf
5cf2653d277045cf2653d27744.pdf
5cf23af705d035cf23af705d42.pdf
5cf23a9995a2a5cf23a9995a3f.pdf
5cb42a990ddc95cb42a990de10.pdf
5c9b4e4ad6a855c9b4e4ad6ac4.pdf
5c8f8013d30da5c8f8013d3119.pdf
5c7fbbbb031c85c7fbbbb03208.pdf
5c5ad529642755c5ad529642b5.pdf
5c5ad4e2acf615c5ad4e2acfa0.pdf
5c3ca66428d365c3ca66428d76.pdf
5c3ca59e3cec55c3ca59e3cf04.pdf
5c3c9b916c22b5c3c9b916c26b.pdf
5c22517a8d0bc5c22517a8d0fc.pdf
5c1104b6c60025c1104b6c602b.pdf
5bf547bddef105bf547bddef4f.pdf
5bd47405708335bd4740570873.pdf
5bd473c27d5935bd473c27d5af.pdf
5bbe1a46393245bbe1a4639360.pdf
5bd1ef9a68d375bd1ef9a68d77.pdf
5bbe19fcd2e805bbe19fcd2ebb.pdf
5bbe18679b9ba5bbe18679b9f5.pdf
5bba2ac82c4ae5bba2ac82c4ea.pdf
592eaafa982a7592eaafa982e0.pdf
5aeddbeca9ca75aeddbeca9ce1.pdf
5abfca28dcf0d5abfca28dcf59.pdf
5abfc9297cde25abfc9297ce1b.pdf
5abfc6574500a5abfc65745044.pdf
5abfc5ff99fb25abfc5ff99ff9.pdf
5abfc5459c4d75abfc5459c511.pdf
5a5cc03ef07b85a5cc03ef07f2.pdf
5a5cac4af3c425a5cac4af3c7f.pdf
5a535204756965a535204756cf.pdf
5a5350a91a41d5a5350a91a461.pdf
5a1421b2f32775a1421b2f32b1.pdf
5a01d213a404f5a01d213a408a.pdf
59f4407891b4659f4407891b80.pdf
59e608242df2059e608242df67.pdf
59e6060d4247d59e6060d424bc.pdf
59e605a6b31f059e605a6b3229.pdf
59a418fdeb71759a418fdeb752.pdf
59a418ab1f7d959a418ab1f815.pdf
59563ad3d78b559563ad3d78ee.pdf
59563b2024bc659563b2024c00.pdf
59563b7a2af6559563b7a2afa1.pdf
5956411d5a6ad5956411d5a6e7.pdf
595641fe7dc1d595641fe7dc47.pdf
59491d76bb8d259491d76bb8f8.pdf
59491d4e5600659491d4e5603f.pdf
5943e7020114e5943e70201188.pdf
5943e6c252c335943e6c252c6e.pdf
5943e67a0ddc95943e67a0de02.pdf
5943e076baf925943e076bafd8.jpeg
593022b76d3f5593022b76d431.jpeg
5930227ebef495930227ebef86.jpeg
590c618798452590c61879848c.pdf
590a12374231d590a12374233d.doc
58faf65f8c9fe58faf65f8ca37.pdf
58a322715d9a258a322715d9ec.pdf
586116a2cb01a586116a2cb054.jpg
586116d3d223b586116d3d2275.jpeg
59203e9f36c0059203e9f36c3c.pdf
585e232bd9b73585e232bd9bbb.jpeg
58297a209e24658297a209e283.djvu
58144c0269eb558144c0269eef.pdf
58144aef8fbfe58144aef8fc38.pdf
58144a2d4fe3358144a2d4fe6d.pdf
570f782c0d5ef570f782c0d629.pdf
570f771b0aae4570f771b0ab1e.pdf
570f761b7f3eb570f761b7f427.pdf
56b9f88c1c32856b9f88c1c362.pdf
56b9f0717ee0656b9f0717ee40.pdf
56a6146e8856f56a6146e885ab.pdf
56a6141bf05ee56a6141bf0629.pdf
56a613c28e17c56a613c28e1b9.pdf
56741bf2493d656741bf249410.pdf
56741baf952c056741baf952fb.pdf
55b0cd2ecccb055b0cd2eccced.jpg
'
  for file in ${files}; do
    curl "http://xn--80aphg2b.xn--p1ai/res/${file}" -H "${H}" -o "${file}"
  done

  for i in $(jot 1000 1000); do
  for i in $(jot 2000 1000); do
  for i in $(jot 1000); do
    url="http://school.mipt.ru/pubFileDown.asp?id=${i}"
    curl "${url}" -I --remote-header-name | grep 'Content-Disposition: attachment; filename=' /dev/stdin >/dev/null
    if [[ $? == "0" ]]; then
      echo "Downloading ${url}"
      curl "${url}" --remote-header-name -O
    fi
  done
}
