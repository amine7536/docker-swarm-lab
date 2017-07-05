FROM ruby:2.1.5

WORKDIR /usr/src/app
COPY Gemfile* ./
RUN bundle install --without development test
COPY . .

EXPOSE 3000
CMD ["bundle", "exec", "ruby", "web.rb", "-s", "Puma", "-p 3000"]
