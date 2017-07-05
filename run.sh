docker service create --name my-feature-ms1 \
    -e MS_URL=http://new-branch-ms2.pix.lab \
    --network apps \
    --network proxy \
    --label com.df.notify=true \
    --label com.df.distribute=true \
    --label com.df.servicePath=/  \
    --label com.df.serviceDomain=my-feature-ms1.pix.lab \
    --label com.df.port=8080 \
    ms1:my-feature


# CLI 

pip install -e .[test]