# Google photo migration

Helps to migrate from Google Photos to other cloud platform. In particular, this script
transfers dates to JPG and PNG images from JSON metafiles.

Deleting jsons:

```find . -type f -name '*.json' -delete```

```find . -type f -name '*(1).*' -delete```

```find . -type f -name '*.json' -print```

```find . -type f -name '*(1).*' -exec du -ch {} + | grep total$```

```find . -type f -name '*.json' -exec du -ch {} + | grep total$```