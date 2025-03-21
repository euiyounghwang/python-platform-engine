# -*- encoding: utf-8 -*-
# stub: logstash-integration-kafka 10.4.0 java lib vendor/jar-dependencies

Gem::Specification.new do |s|
  s.name = "logstash-integration-kafka".freeze
  s.version = "10.4.0"
  s.platform = "java".freeze

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.metadata = { "integration_plugins" => "logstash-input-kafka,logstash-output-kafka", "logstash_group" => "integration", "logstash_plugin" => "true" } if s.respond_to? :metadata=
  s.require_paths = ["lib".freeze, "vendor/jar-dependencies".freeze]
  s.authors = ["Elastic".freeze]
  s.date = "2020-07-03"
  s.description = "This gem is a Logstash plugin required to be installed on top of the Logstash core pipeline using $LS_HOME/bin/logstash-plugin install gemname. This gem is not a stand-alone program.".freeze
  s.email = "info@elastic.co".freeze
  s.homepage = "http://www.elastic.co/guide/en/logstash/current/index.html".freeze
  s.licenses = ["Apache-2.0".freeze]
  s.rubygems_version = "3.0.6".freeze
  s.summary = "Integration with Kafka - input and output plugins".freeze

  s.installed_by_version = "3.0.6" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_development_dependency(%q<jar-dependencies>.freeze, [">= 0.3.12"])
      s.add_runtime_dependency(%q<logstash-core-plugin-api>.freeze, [">= 1.60", "<= 2.99"])
      s.add_runtime_dependency(%q<logstash-core>.freeze, [">= 6.5.0"])
      s.add_runtime_dependency(%q<logstash-codec-json>.freeze, [">= 0"])
      s.add_runtime_dependency(%q<logstash-codec-plain>.freeze, [">= 0"])
      s.add_runtime_dependency(%q<stud>.freeze, [">= 0.0.22", "< 0.1.0"])
      s.add_development_dependency(%q<logstash-devutils>.freeze, [">= 0"])
      s.add_development_dependency(%q<rspec-wait>.freeze, [">= 0"])
      s.add_development_dependency(%q<ruby-kafka>.freeze, [">= 0"])
      s.add_development_dependency(%q<snappy>.freeze, [">= 0"])
    else
      s.add_dependency(%q<jar-dependencies>.freeze, [">= 0.3.12"])
      s.add_dependency(%q<logstash-core-plugin-api>.freeze, [">= 1.60", "<= 2.99"])
      s.add_dependency(%q<logstash-core>.freeze, [">= 6.5.0"])
      s.add_dependency(%q<logstash-codec-json>.freeze, [">= 0"])
      s.add_dependency(%q<logstash-codec-plain>.freeze, [">= 0"])
      s.add_dependency(%q<stud>.freeze, [">= 0.0.22", "< 0.1.0"])
      s.add_dependency(%q<logstash-devutils>.freeze, [">= 0"])
      s.add_dependency(%q<rspec-wait>.freeze, [">= 0"])
      s.add_dependency(%q<ruby-kafka>.freeze, [">= 0"])
      s.add_dependency(%q<snappy>.freeze, [">= 0"])
    end
  else
    s.add_dependency(%q<jar-dependencies>.freeze, [">= 0.3.12"])
    s.add_dependency(%q<logstash-core-plugin-api>.freeze, [">= 1.60", "<= 2.99"])
    s.add_dependency(%q<logstash-core>.freeze, [">= 6.5.0"])
    s.add_dependency(%q<logstash-codec-json>.freeze, [">= 0"])
    s.add_dependency(%q<logstash-codec-plain>.freeze, [">= 0"])
    s.add_dependency(%q<stud>.freeze, [">= 0.0.22", "< 0.1.0"])
    s.add_dependency(%q<logstash-devutils>.freeze, [">= 0"])
    s.add_dependency(%q<rspec-wait>.freeze, [">= 0"])
    s.add_dependency(%q<ruby-kafka>.freeze, [">= 0"])
    s.add_dependency(%q<snappy>.freeze, [">= 0"])
  end
end
