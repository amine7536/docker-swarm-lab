# docker service create --name my-feature-ms1 \
#     -e MS_URL=http://new-branch-ms2.pix.lab \
#     --network apps \
#     --network proxy \
#     --label com.df.notify=true \
#     --label com.df.distribute=true \
#     --label com.df.servicePath=/  \
#     --label com.df.serviceDomain=my-feature-ms1.pix.lab \
#     --label com.df.port=3000 \
#     ms1:my-feature


# # CLI 

# pip install -e .[test]


docker service create --name hello-world \
     -e MS_URL=http://new-branch-ms2.pix.lab \
     --network apps \
     --network proxy \
     --label com.df.notify=true \
     --label com.df.distribute=true \
     --label com.df.servicePath=/  \
     --label com.df.serviceDomain=hello.pix.lab \
     --label com.df.port=3000 \
     sixeyed/docker-swarm-walktrough