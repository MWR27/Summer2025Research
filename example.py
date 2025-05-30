from clusters import Clusters

clusters_a = Clusters.create_monomers(100)
print(f'Original (Size {clusters_a.particle_count()}):\n', clusters_a)
successful_collisions = clusters_a.collide(50)
print(f'After {successful_collisions} collisions (Size {clusters_a.particle_count()}):\n', clusters_a)
print()

clusters_b = Clusters({2: 100000})
print(f'Original (Size {clusters_b.particle_count()}):\n', clusters_b)
successful_collisions = clusters_b.collide(50000, 1)
print(f'After {successful_collisions} collisions (Size {clusters_b.particle_count()}):\n', clusters_b)
print('Size:', clusters_b.particle_count())
