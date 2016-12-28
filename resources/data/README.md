= 资源文件

分为两种资源类型：txt和csv类型

== TXT 文件


== csv 文件

这几个文件主要是经度纬度信息、以及streets的types信息，用来作为ontology的addinfo内容
stops.borough.locations.csv 公交站-行政区对应关系，多对一关系。用来生成ontology["addinfo"]["borough"]内容、以及ontology["compatible_values"]["borough_stop"]内容
stops.locations.csv 公交站-城市对应关系，一对多关系。用来生成ontology["addinfo"]["city"]内容；同时生成ontology["compatible_value"]["city_stop"]内容。
cities.locations.csv 城市-州对应关系，可能多个州里面都有一个相同的城市名，因此城市-州对应关系是，一对多。用来生成ontology["addinfo"]["state"]内容。同时，用来生成ontology["compatible_value"]["city_state"]内容。
streets.types.csv 街道-行政区对应关系，以及街道类型（街、道）。用来生成ontology["addinfo"]["street_type"]内容。同时，用来生成ontology["compatible_value"]["borough_street"]内容。