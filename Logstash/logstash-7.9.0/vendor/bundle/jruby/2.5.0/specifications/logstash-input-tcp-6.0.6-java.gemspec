# -*- encoding: utf-8 -*-
# stub: logstash-input-tcp 6.0.6 java lib vendor/jar-dependencies

Gem::Specification.new do |s|
  s.name = "logstash-input-tcp".freeze
  s.version = "6.0.6"
  s.platform = "java".freeze

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.metadata = { "logstash_group" => "input", "logstash_plugin" => "true" } if s.respond_to? :metadata=
  s.require_paths = ["lib".freeze, "vendor/jar-dependencies".freeze]
  s.authors = ["Elastic".freeze]
  s.date = "2020-06-03"
  s.description = "This gem is a Logstash plugin required to be installed on top of the Logstash core pipeline using $LS_HOME/bin/logstash-plugin install gemname. This gem is not a stand-alone program".freeze
  s.email = "info@elastic.co".freeze
  s.homepage = "http://www.elastic.co/guide/en/logstash/current/index.html".freeze
  s.licenses = ["Apache License (2.0)".freeze]
  s.rubygems_version = "3.0.6".freeze
  s.summary = "Reads events from a TCP socket".freeze

  s.installed_by_version = "3.0.6" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_runtime_dependency(%q<logstash-core-plugin-api>.freeze, [">= 1.60", "<= 2.99"])
      s.add_runtime_dependency(%q<logstash-codec-plain>.freeze, [">= 0"])
      s.add_runtime_dependency(%q<logstash-codec-line>.freeze, [">= 0"])
      s.add_runtime_dependency(%q<logstash-codec-json>.freeze, [">= 0"])
      s.add_runtime_dependency(%q<logstash-codec-json_lines>.freeze, [">= 0"])
      s.add_runtime_dependency(%q<logstash-codec-multiline>.freeze, [">= 0"])
      s.add_development_dependency(%q<logstash-devutils>.freeze, [">= 0"])
      s.add_development_dependency(%q<insist>.freeze, [">= 0"])
      s.add_development_dependency(%q<flores>.freeze, ["~> 0.0.6"])
      s.add_development_dependency(%q<stud>.freeze, ["~> 0.0.22"])
    else
      s.add_dependency(%q<logstash-core-plugin-api>.freeze, [">= 1.60", "<= 2.99"])
      s.add_dependency(%q<logstash-codec-plain>.freeze, [">= 0"])
      s.add_dependency(%q<logstash-codec-line>.freeze, [">= 0"])
      s.add_dependency(%q<logstash-codec-json>.freeze, [">= 0"])
      s.add_dependency(%q<logstash-codec-json_lines>.freeze, [">= 0"])
      s.add_dependency(%q<logstash-codec-multiline>.freeze, [">= 0"])
      s.add_dependency(%q<logstash-devutils>.freeze, [">= 0"])
      s.add_dependency(%q<insist>.freeze, [">= 0"])
      s.add_dependency(%q<flores>.freeze, ["~> 0.0.6"])
      s.add_dependency(%q<stud>.freeze, ["~> 0.0.22"])
    end
  else
    s.add_dependency(%q<logstash-core-plugin-api>.freeze, [">= 1.60", "<= 2.99"])
    s.add_dependency(%q<logstash-codec-plain>.freeze, [">= 0"])
    s.add_dependency(%q<logstash-codec-line>.freeze, [">= 0"])
    s.add_dependency(%q<logstash-codec-json>.freeze, [">= 0"])
    s.add_dependency(%q<logstash-codec-json_lines>.freeze, [">= 0"])
    s.add_dependency(%q<logstash-codec-multiline>.freeze, [">= 0"])
    s.add_dependency(%q<logstash-devutils>.freeze, [">= 0"])
    s.add_dependency(%q<insist>.freeze, [">= 0"])
    s.add_dependency(%q<flores>.freeze, ["~> 0.0.6"])
    s.add_dependency(%q<stud>.freeze, ["~> 0.0.22"])
  end
end
