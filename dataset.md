# Notes on the MSD Dataset 

Engelenburg, Casper van, Fatemeh Mostafavi, Emanuel Kuhn, et al. “MSD: A Benchmark Dataset for Floor Plan Generation of Building Complexes.” arXiv:2407.10121. Preprint, arXiv, July 24, 2024. https://doi.org/10.48550/arXiv.2407.10121.

[Link to dataset](https://www.kaggle.com/datasets/caspervanengelenburg/modified-swiss-dwellings)

----

## Definitions 

**Entity**: A  row in the dataset that has some geometry associated with it 

#### Identifiers

- **Site ID**: Describes the site (neighborhood) where the entity is located 
  - Buildings on the same site may share similar characteristics 
  - *Does the original Swiss dwellings dataset show the locations of different sites?*
- **Building ID**: Describes the building where the entity is located 
- **Plan ID**: Describes the floor plan layout "prototype" the entity is part of  
- **Floor ID**: Describes the particular floor (at a specific elevation) in a building that an entity is located on 
- **Apartment ID**: Describes which apartment the entity emerges from 
  - Apartment ID is shared for multi-story apartments that stretch across multiple levels.. 
  - *(is this still relevant in the data analysis? Or should the plan ID be preferred?)*
  - 
- **Unit ID**: Also says the apartment the entity comes from, but is different for different floor 


## Unit IDs
[(48475.0,), (48489.0,), (48885.0,), (48887.0,), (48890.0,), (48892.0,), (48894.0,), (48898.0,), (48904.0,), (48906.0,), (48907.0,), (48909.0,)]
