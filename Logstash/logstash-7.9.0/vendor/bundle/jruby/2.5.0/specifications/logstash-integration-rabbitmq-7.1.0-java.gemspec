# -*- encoding: utf-8 -*-
# stub: logstash-integration-rabbitmq 7.1.0 java lib

Gem::Specification.new do |s|
  s.name = "logstash-integration-rabbitmq".freeze
  s.version = "7.1.0"
  s.platform = "java".freeze

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.metadata = { "integration_plugins" => "logstash-input-rabbitmq,logstash-output-rabbitmq", "logstash_group" => "integration", "logstash_plugin" => "true" } if s.respond_to? :metadata=
  s.require_paths = ["lib".freeze]
  s.authors = ["Elastic".freeze]
  s.date = "2020-05-13"
  s.description = "This gem is a Logstash plugin required to be installed on top of the Logstash core pipeline using $LS_HOME/bin/logstash-plugin install gemname. This gem is not a stand-alone program.".freeze
  s.email = "info@elastic.co".freeze
  s.homepage = "http://www.elastic.co/guide/en/logstash/current/index.html".freeze
  s.licenses = ["Apache License (2.0)".freeze]
  s.rubygems_version = "3.0.6".freeze
  s.summary = "Integration with RabbitMQ - input and output plugins".freeze

  s.installed_by_version = "3.0.6" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_runtime_dependency(%q<logstash-core-plugin-api>.freeze, [">= 1.60", "<= 2.99"])
      s.add_runtime_dependency(%q<logstash-core>.freeze, [">= 6.5.0"])
      s.add_runtime_dependency(%q<logstash-codec-json>.freeze, [">= 0"])
      s.add_runtime_dependency(%q<march_hare>.freeze, ["~> 4.0"])
      s.add_runtime_dependency(%q<stud>.freeze, ["~> 0.0.22"])
      s.add_runtime_dependency(%q<back_pressure>.freeze, ["~> 1.0"])
      s.add_development_dependency(%q<logstash-devutils>.freeze, ["~> 2.0"])
      s.add_development_dependency(%q<logstash-input-generator>.freeze, [">= 0"])
      s.add_development_dependency(%q<logstash-codec-plain>.freeze, [">= 0"])
    else
      s.add_dependency(%q<logstash-core-plugin-api>.freeze, [">= 1.60", "<= 2.99"])
      s.add_dependency(%q<logstash-core>.freeze, [">= 6.5.0"])
      s.add_dependency(%q<logstash-codec-json>.freeze, [">= 0"])
      s.add_dependency(%q<march_hare>.freeze, ["~> 4.0"])
      s.add_dependency(%q<stud>.freeze, ["~> 0.0.22"])
      s.add_dependency(%q<back_pressure>.freeze, ["~> 1.0"])
      s.add_dependency(%q<logstash-devutils>.freeze, ["~> 2.0"])
      s.add_dependency(%q<logstash-input-generator>.freeze, [">= 0"])
      s.add_dependency(%q<logstash-codec-plain>.freeze, [">= 0"])
    end
  else
    s.add_dependency(%q<logstash-core-plugin-api>.freeze, [">= 1.60", "<= 2.99"])
    s.add_dependency(%q<logstash-core>.freeze, [">= 6.5.0"])
    s.add_dependency(%q<logstash-codec-json>.freeze, [">= 0"])
    s.add_dependency(%q<march_hare>.freeze, ["~> 4.0"])
    s.add_dependency(%q<stud>.freeze, ["~> 0.0.22"])
    s.add_dependency(%q<back_pressure>.freeze, ["~> 1.0"])
    s.add_dependency(%q<logstash-devutils>.freeze, ["~> 2.0"])
    s.add_dependency(%q<logstash-input-generator>.freeze, [">= 0"])
    s.add_dependency(%q<logstash-codec-plain>.freeze, [">= 0"])
  end
end
