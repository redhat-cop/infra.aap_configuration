if [ -z "$(ls changelogs/fragments/*.yml changelogs/fragments/*.yaml)" ]; then
  echo "change_present=false" >> "$GITHUB_OUTPUT"
else
  echo "change_present=true" >> "$GITHUB_OUTPUT"
fi

grep -RE '(major_changes|breaking_changes)' changelogs/fragments;
MAJOR=$?;
grep -R minor_changes changelogs/fragments;
MINOR=$?;

if [ $MAJOR -eq 0 ]; then
  echo "level=major" >> "$GITHUB_OUTPUT"
  echo "Determined change level: major"
elif [ $MINOR -eq 0 ]; then
  echo "level=minor" >> "$GITHUB_OUTPUT"
  echo "Determined change level: minor"
else
  echo "level=patch" >> "$GITHUB_OUTPUT"
  echo "Determined change level: patch"
fi
