"""
Herein are the parent and component parts that make up an asset Work Unit.

A work unit is any unit of work the artist has produced: model, animation,
shader, texture, rig, groom, etc. It is also the primary object hierarchy
for asset tracking and composition within the core pipeline infrastructure.

Work units can contain nested work units. For example: An asset work unit could
contain shader work units, which themselves could contain texture work units.
"""
