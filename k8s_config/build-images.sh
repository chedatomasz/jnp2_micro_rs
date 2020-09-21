docker build -t gcr.io/jnp2-micrors/users ../users
docker push gcr.io/jnp2-micrors/users

docker build -t gcr.io/jnp2-micrors/items ../items
docker push gcr.io/jnp2-micrors/items

docker build -t gcr.io/jnp2-micrors/front ../front
docker push gcr.io/jnp2-micrors/front

docker build -t gcr.io/jnp2-micrors/ratings ../ratings
docker push gcr.io/jnp2-micrors/ratings

docker build -t gcr.io/jnp2-micrors/recommendations ../recommendations
docker push gcr.io/jnp2-micrors/recommendations

docker build -t gcr.io/jnp2-micrors/recommendations-worker ../recommendations_worker
docker push gcr.io/jnp2-micrors/recommendations-worker



