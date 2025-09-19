{{- define "app-chart.name" -}}
app-chart
{{- end -}}

{{- define "app-chart.fullname" -}}
{{- printf "%s" (include "app-chart.name" .) -}}
{{- end -}}