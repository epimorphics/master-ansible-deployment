# Alerts

## Prometheus Targets

Prometheus generated Alerts.

### Logging Down

No new records indexed for 10 minutes.

#### Details

    - alert: Logging Down
      expr: rate(elasticsearch_indices_indexing_index_total{cluster="docker-cluster"}[1m]) == 0
      for: 10m
      labels:
        severity: critical
      annotations:
        message: "Logging Down"

### Elasticsearh Critical

Elasticsearch cluster is reporting critial error

#### Details

  - alert: Elasticsearh Critical
    expr: elasticsearch_cluster_health_status{cluster="docker-cluster", color="red", job="elasticsearch"} > 0
    for: 10m
    labels:
      severity: critical
    annotations:
      runbook_url: "https://github.com/epimorphics/master-ansible-deployment/blob/main/roles/metrics/templates/prometheus-rules/Readme.md#elasticsearch-critical"


### Elasticsearh Warning

Elasticsearch cluster is reporting a problem

#### Details

    - alert: Elasticsearh Warning
      expr: elasticsearch_cluster_health_status{cluster="docker-cluster", color="yellow", job="elasticsearch"} > 0
      for: 10m
      labels:
        severity: warning
      annotations:
        runbook_url: "https://github.com/epimorphics/master-ansible-deployment/blob/main/roles/metrics/templates/prometheus-rules/Readme.md#elasticsearch-warning"

### Target Down

#### Details

    - alert: Target Down
      expr: up < 1
      for: 3m
      labels:
        severity: critical
      annotations:
        message: "Prometheus Targets Down: {{ $value }}" 

### Absolute Disk Usage Warning

Absolute Disk usage over {{ prom_rules.absolute.disk.warning }}%.

#### Details

    - alert: AbsoluteDiskUsageWarning
      expr: disk_used_percent > {{ prom_rules.absolute.disk.warning }} and disk_user_percent < {{ prom_rulese.absolute.disk.critical }}
      labels:
        severity: warning
      annotations:
        message: "Absolute Disk Usage Warning: {{ $labels.host }}:{{ $labels.path }} at {{ $value }}"

### Absolute Disk Usage Critical

Absolute Disk usage over {{ prom_rules.absolute.disk.critical }}%.

#### Details

    - alert: AbsoluteDiskUsageCritical
      expr: disk_used_percent >= {{ prom_rules.absolute.disk.critical }}
      labels:
        severity: critical
      annotations:
        message: "Absolute Disk Usage Critical: {{ $labels.host }}:{{ $labels.path }} at {{ $value }}"

### Projected Disk Usage Warning

Projected Disk usage over previous {{ prom_rules.disk.projected.warning }} is unsustainable.

#### Details

    - alert: ProjectedDiskUsageWarning
      expr: disk_free+delta(disk_free[{{ prom_rules.projected_disk.projectedwarning }}]) < 0
      labels:
        severity: warning
      annotations:
        message: "Projected Disk Usage Warning: {{ $labels.host }}:{{ $labels.path }}"

### Projected Disk Usage Critical

Projected Disk usage over previous {{ prom_rules.disk.projected.critical }} is unsustainable.

#### Details

    - alert: ProjectedDiskUsageCritical
      expr: disk_used_percent >= {{ prom_rules.inode.critical }}
      expr: disk_free+delta(disk_free[{{ prom_rules.disk.projection.critical}}]) < 0
      labels:
        severity: critical
      annotations:
        message: "Projected Disk Usage Critical: {{ $labels.host }}:{{ $labels.path }}"

### Absolute Inode Usage Warning

Absolute Inode usage over {{ prom_rulese.absolute.inode.warning }}%.

#### Details

    - alert: AbsoluteInodeUsageWarning
      expr: ( 100*disk_inodes_used{fstype!="xfs"}/disk_inodes_total ) > {{ prom_rules.absolute.inode.warning }} and ( 100*disk_inodes_used{fstype!="xfs"}/disk_inodes_total ) < {{ prom_rules.absolute.inode.critical }}
      labels:
        severity: warning
      annotations:
        message: "Inode Usage Warning: {{ $labels.host }}:{{ $labels.path }} at {{ $value }}"

### Absolute Inode Usage Critical

Absolute Inode usage over {{ prom_rules.absolute.inode.critical }}%.

#### Details

    - alert: AbsoluteInodeUsageCritical
      expr: ( 100*disk_inodes_used{fstype!="xfs"}/disk_inodes_total ) >= {{ prom_rules.absolute.inode.critical }}
      labels:
        severity: critical
      annotations:
        message: "Inode: Usage Critical: {{ $labels.host }}:{{ $labels.path }} at {{ $value }}"

### Projected Inode Usage Warning

Projected Inode usage over previous {{ prom_rules.projected.warning }} is unsustainable.

#### Details

    - alert: ProjectedInodeUsageWarning
      expr: disk_inodes_free{fstype!="xfs"}+delta(disk_inodes_free{fstype!="xfs"}[{{ prom_rules.projected.warning }}]) < 0
      labels:
        severity: warning
      annotations:
        message: "Projected Inode Usage Warning: {{ $labels.host }}:{{ $labels.path }}"

### Projected Inode Usage Critical

Projected Inode usage over previous {{ prom_rules.projected.critical }} is unsustainable.

#### Details

    - alert: ProjectedInodeUsageCritical
      expr: disk_inodes_free{fstype!="xfs"}+delta(disk_inodes_free{fstype!="xfs"}[{{ prom_rules.projected.critical }}]) < 0
      labels:
        severity: critical
      annotations:
        message: "Projected Inode: Usage Critical: {{ $labels.host }}:{{ $labels.path }}"

### System Load Warning

System load within one cpu core of limit

#### Details

    - alert: System Load Warning
      expr: system_load1>(system_n_cpus-1)
      for: 15m
      labels:
        severity: warning
      annotations:
        message: "System load within one cpu core of limit"

### System Load Critical

System load within half cpu core of limit

#### Details

    - alert: System Load Critical
      expr: system_load1>(system_n_cpus-0.5)
      for: 15m
      labels:
        severity: critical
      annotations:
        message: "System load within half cpu core of limit"

### Container Stopped

#### Details

    - alert: Container Stopped
      expr: docker_n_containers_stopped > 1
      labels:
        severity: critical
      annotations:
        message: "Docker Container Stopped on host {{ $labels.host }}"

## Ruby Applicaiton Errors

### APIConnectionError

#### Details

    - alert: APIConnectionError
      expr: rate(api_connection_failure[10m]) > 0
      labels:
        severity: critical
      annotations:
        message: "API Connection Error: {{ $labels.job }} - {{ $labels.host }}"


### APIServiceException

#### Details

    - alert: APIServiceException
      expr: rate(api_service_exception[10m]) > 0
      labels:
        severity: critical
      annotations:
        message: "API Service Exception: {{ $labels.job }} - {{ $labels.host }}"


### APIStatus

#### Details

    - alert: APIStatus
      expr: rate(api_status{status=~"[45].."}[10m]) > 0
      labels:
        severity: warning
      annotations:
        message: "Unexpected API status return {{ $labels.status }}: {{ $labels.job }} - {{ $labels.host }}"


### APIRequestFailures

#### Details

    - alert: APIRequestFailures
      expr: rate(api_requests{result!="success"}[10m]) > 0
      labels:
        severity: critical
      annotations:
        message: "API Request Failure: {{ $labels.result }}: {{ $labels.job }} - {{ $labels.host }}"


### ApplicationInternalError

#### Details

    - alert: ApplicationInternalError
      expr: rate(internal_application_error[10m]) > 0
      labels:
        severity: critical
      annotations:
        message: "Internal Application Error: {{ $labels.job }} - {{ $labels.host }}\n{{ $labels.message }}"
