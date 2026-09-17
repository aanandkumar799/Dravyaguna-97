# DravyaGuna 97 — Local Plant Image Library

Plant photography is stored separately from application code.

```text
images/
└── plants/
    └── <plant-id>/
        ├── whole_plant/image.*
        ├── habit/image.*
        ├── root/image.*
        ├── stem/image.*
        ├── leaf/image.*
        ├── flower/image.*
        ├── fruit/image.*
        ├── seed/image.*
        └── bark/image.*
```

The automated image audit downloads only high-confidence, exact-species, part-specific, openly licensed images and records the source, author and license in `data/curated-image-manifest.json`. Missing parts remain explicitly unresolved rather than being filled with unrelated images.
