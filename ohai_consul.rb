require 'json'
require 'net/http'
require 'base64'

Ohai.plugin(:Consul) do
  provides 'consul'

  def merge_hash(h1, h2)
    h1.merge(h2) {|k, v1, v2| merge_hash(v1, v2) }
  end

  collect_data do
    uri = URI('http://localhost:8500/v1/kv/hpaas?recurse')
    response = Net::HTTP.get(uri)
    kv_items = JSON.parse(response)

    build_hash = {}

    kv_items.each do |kv_item|
      key = kv_item['Key'].split('/')
      value = Base64.decode64(kv_item['Value'])
      h = key.reverse.inject(value) { |a, n| { n => a } }
      build_hash = merge_hash(build_hash, h)
    end

    consul build_hash

    cookbook_hash = {'consul' => build_hash}
    cookbook_json = JSON.pretty_generate(cookbook_hash)
    file_name = '/tmp/cookbook_consul.json'
    File.open(file_name, 'w') { |fd| fd.write(cookbook_json) }
  end
end
