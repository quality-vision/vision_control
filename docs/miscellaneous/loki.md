# Feature tracking with Loki

The [provided Loki dashboards](../grafana/gallery.md#loki) tracks usage of features by parsing tags from log messages. For this to work, you need to add some extra tags to your log messages.

## Tags

| Tag               | Type      | Required | Description                                               |
|-------------------|:---------:|:--------:|-----------------------------------------------------------|
| `feature`         | `string`  | yes      | Name of the feature to track.                             |
| `step`            | `integer` | yes      | Interaction step.                                         |
| `step_definition` | `string`  | yes      | Textual description of the current interaction step.      |
| `final_step`      | `boolean` | yes      | Whether this is the final step of the interaction or not. |
| `new_tag`         | `uuid`    | yes      | Randomly generated identifier of the interaction. Used to stop Loki from aggregating logs. Might not be needed.|

## Example

The following example shows how to track features in Python.

!!! note
    In the example below, we use the log message as a step description instead of `step_definition`. The provided panels use `step_definition`, but we recommend that you deprecate that tag and use the log message instead for logs that is easier to read and understand.

```python
    log.debug("User clicked on 'Pay with Swish'.",
        extra={
            "tags": {
                "company": "Karls Buffé",
                "feature": "swish-payment",
                "step": 1,
                "final_step": False,
            }
        },
    )

    log.debug("User entered their phone number.",
        extra={
            "tags": {
                "company": "Karls Buffé",
                "feature": "swish-payment",
                "step": 2,
                "final_step": False,
            }
        },
    )

    log.debug("User authorized the purchase via Swish on their phone.",
        extra={
            "tags": {
                "company": "Karls Buffé",
                "feature": "swish-payment",
                "step": 3,
                "final_step": True,
            }
        },
    )
```
