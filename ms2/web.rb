require 'sinatra'
require 'net/http'
require 'uri'

get '/' do
  uri = URI(ENV['MS_URL'])
  http = Net::HTTP.new(uri.host, uri.port)
  response = http.request(Net::HTTP::Get.new(uri.request_uri))
  status = response.code == '200' ? 'OK', 'NOK'
  
  "Hello, world. I'm #{status}\n"
end
