import raw from './lessons.json';
import {lessonSchema} from '../types/content';
import {practiceAdditions} from './practice-additions';

// Preserve published URLs and exercise IDs so saved student progress remains valid.
// The 51-section curriculum map is an authoring plan, not verified lesson content.
export const expandedLessons=raw.map(lesson=>lessonSchema.parse({
 ...lesson,
 exercises:[...lesson.exercises,...practiceAdditions[lesson.id]],
}));
